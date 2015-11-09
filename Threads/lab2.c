/*
*  Joseph DeBruycker
*  Assignment 2
*  CSCI 460
*  Fall 2015
*/

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int BUFFER_MAX = 20;
int buffer_size = 0;
time_t t;
pthread_mutex_t mymutex = PTHREAD_MUTEX_INITIALIZER;

// Doubly linked list nodes
struct node {
	int value;
	struct node* next;
	struct node* prev;
};

// Variables for referencing our buffer
struct node* bhead;
struct node* btail;

// Creates 3 nodes of a doubly linked list
initialize_buffer(){
	// Create first node in list
	bhead = malloc(sizeof(struct node));
	// Last node = first node for now
	btail = bhead;
	// Initialize values of first node
	bhead->next = 0;
	bhead->prev = 0;
	bhead->value = rand() % 40;
	//printf("%d\n", bhead->value);
	
	// Node 2
	btail->next = malloc(sizeof(struct node));
	btail = btail->next;
	btail->next = 0;
	btail->prev = bhead;
	btail->value = rand() % 40;
	//printf("%d\n", btail->value);
	
	// Node 3
	btail->next = malloc(sizeof(struct node));
	btail->next->prev = btail;
	btail = btail->next;
	btail->next = 0;
	btail->value = rand() % 40;
	//printf("%d\n", btail->value);
	buffer_size = 3;
	return;
}

// Iterate through all nodes printing their values
print_buffer(){
	struct node* printer;
	printer = bhead;
	printf("\nBuffer size: %d\n", buffer_size);
	printf("Values: ");
	while(printer != 0){
		printf("%d ", printer->value);
		printer = printer->next;
	}
}

// Producer 1 generates a new node at the end of the buffer with an odd value
produce1(){
	int i;
	for(i=0;i<10;i++){
		pthread_mutex_lock(&mymutex);
		if(buffer_size<BUFFER_MAX){
			printf("\nProducer 1 Running");
			print_buffer();
			struct node* new_node = malloc(sizeof(struct node));
			int new_value = rand()%39;
			if((new_value%2)==0){
				new_value++;
			}
			new_node->value = new_value;
			new_node->next = 0;
			// Special case if list is empty:
			if(buffer_size==0){
				new_node->prev = 0;
				bhead = new_node;
			} else {
				new_node->prev = btail;
				btail->next = new_node;
			}
			btail = new_node;
			buffer_size++;
			print_buffer();
		} else {
			printf("\nBuffer overflow on Producer 1!");
		}
		pthread_mutex_unlock(&mymutex);
		sleep(1);
	}
	return;
}

// Producer 2 generates a new node at the end of the buffer with an even value
produce2(){
	int i;
	for(i=0;i<10;i++){
		pthread_mutex_lock(&mymutex);
		if(buffer_size<BUFFER_MAX){
			printf("\nProducer 2 Running");
			print_buffer();
			struct node* new_node = malloc(sizeof(struct node));
			int new_value = rand()%39;
			if((new_value%2)!=0){
				new_value++;
			}
			new_node->value = new_value;
			new_node->next = 0;
			// Special case if list is empty:
			if(buffer_size==0){
				new_node->prev = 0;
				bhead = new_node;
			} else {
				new_node->prev = btail;
				btail->next = new_node;
			}
			btail = new_node;
			buffer_size++;
			print_buffer();
		} else {
			printf("\nBuffer overflow on Producer 2!");
		}
		pthread_mutex_unlock(&mymutex);
		sleep(1);
	}
	return;
}

// Consumer 1 consumes the first node from the list if its value is odd
consume1(){
	int i;
	for(i=0;i<10;i++){
		pthread_mutex_lock(&mymutex);
		printf("\nConsumer 1 Running");
		if(buffer_size>1){
			if(((bhead->value)%2)!=0){
				print_buffer();
				bhead = bhead->next;
				free(bhead->prev);
				bhead->prev = 0;
				buffer_size--;
				print_buffer();
			}
		} else if(buffer_size==1){
			if(((bhead->value)%2)!=0){
				print_buffer();
				free(bhead);
				bhead = 0;
				buffer_size--;
				print_buffer();
			}
		} else {
			printf("\nBuffer underflow on Consumer 1!");
		}
		pthread_mutex_unlock(&mymutex);
		sleep(1);
	}
	return;
}

// Consumer 2 consumes the first node from the list if its value is even
consume2(){
	int i;
	for(i=0;i<10;i++){
		pthread_mutex_lock(&mymutex);
		printf("\nConsumer 2 Running");
		if(buffer_size>1){
			if(((bhead->value)%2)==0){
				print_buffer();
				bhead = bhead->next;
				free(bhead->prev);
				bhead->prev = 0;
				buffer_size--;
				print_buffer();
			}
		} else if(buffer_size==1){
			if(((bhead->value)%2)==0){
				print_buffer();
				free(bhead);
				bhead = 0;
				buffer_size--;
				print_buffer();
			}
		} else {
			printf("\nBuffer underflow on Consumer 2!");
		}
		pthread_mutex_unlock(&mymutex);
		sleep(1);
	}
	return;
}

int main(){
	// Initialize random num generator
	srand((unsigned) time(&t));
	// Make an initial buffer of 3 nodes
	initialize_buffer();
	print_buffer();
	
	// Start threads 
	pthread_t thread1, thread2, thread3, thread4;
	int tid1 = pthread_create(&thread1,NULL,(void *)produce1, (void *)0);
	if (tid1 < 0 ) printf("1st thread_create failure.\n");
	int tid2 = pthread_create(&thread2,NULL,(void *)produce2, (void *)0);
	if (tid2 < 0 ) printf("2nd thread_create failure.\n");
	int tid3 = pthread_create(&thread3,NULL,(void *)consume1, (void *)0);
	if (tid3 < 0 ) printf("3rd thread_create failure.\n");
	int tid4 = pthread_create(&thread4,NULL,(void *)consume2, (void *)0);
	if (tid4 < 0 ) printf("4th thread_create failure.\n");
	
	// Wait for threads to finish
	pthread_join(thread1,NULL);
	pthread_join(thread2,NULL);
	pthread_join(thread3,NULL);
	pthread_join(thread4,NULL);
	
	// Release mutex variable
	pthread_mutex_destroy(&mymutex);
	
	// Exit
	return 0;
	
}