/*
 * This is a PoC sample
 *
 */

/* headers */
#include <stdio.h>
#include <string.h>


/* global variables and macros */
#define VULNERABLE      7
#define NOT_VULNERABLE  0

int func(){
    return 1;
}


/* functions */
int check(int argc, char **argv){
    int res = NOT_VULNERABLE;

    if(func() == 1)
        return VULNERABLE;
    else
        return NOT_VULNERABLE;

}


int main(int argc, char **argv){
    return check(argc, argv);
}