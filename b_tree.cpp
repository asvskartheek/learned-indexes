#include<iostream>
#include<vector>
#include<stdlib.h>

#define NODE_SIZE 5 

typedef struct _node{
    int value;
    struct _node * left;
    struct _node * right;
}_node;

typedef struct b_node{
    std::vector<_node*> nodes;
    struct b_node * left;
    struct b_node * right;
}b_node;

_node * create_node(int value){
    _node * temp = (_node *) malloc(sizeof(_node));
    temp->value = value;
    temp->left = NULL;
    temp->right = NULL;

    return temp;
}

void insert(b_node * root, int value){
    if(root==NULL){
        root = (b_node*) malloc(sizeof(b_node));
        root->nodes.reserve(NODE_SIZE);
    }
    _node * temp = create_node(value);
    root->nodes.push_back(temp);
}

int main(){
    b_node * root = NULL;
    insert(root,12);
}