#include<stdio.h>
#include<stdlib.h>

#define NODE_SIZE 5 

typedef struct b_node{
    int value;
    struct b_node * left;
    struct b_node * right;
}b_node;