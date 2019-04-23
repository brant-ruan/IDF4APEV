/*
 * This is a PoC sample
 *
 */

/* headers */
#include <stdio.h>
#include <string.h>
#include "idf.h"

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