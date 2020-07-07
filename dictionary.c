// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 150000;

// Hash table
node *table[N];

// Number of Words Loaded From Dictionary
int WORD_COUNT = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Hash word to obtain a hash value
    int index = hash(word);

    // Access linked list at that index in the hash table
    node *head = table[index];
    
    // If there is nothing at this location in the hash table
    if (head == NULL)
    {
        return false;
    }
    
    // If the word is stored in the first node
    if (strcasecmp(head->word, word) == 0)
    {
        return true;
    }
    
    // Traverse linked list, looking for the word (strcasecmp)
    for (node *cursor = head->next; cursor != NULL; cursor = cursor->next)
    {
        // End of the linked list
        if (cursor == NULL)
        {
            return false;
        }
        
        // If the word matches the word in this node
        else if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
    }
    
    // Word was not found
    return false;
}


// Hashes word to a number
unsigned int hash(const char *word)
{
    /*
    * A case-insensitive implementation of the djb2 hash function.
    * by Neel Mehta at
    * https://github.com/hathix/cs50-section/blob/master/code/7/sample-hash-functions/good-hash-function.c
    */
    unsigned long x = 5381;

    // Utilise each character in the word
    for (const char *ptr = word; *ptr != '\0'; ptr++)
    {
        x = ((x << 5) + x) + tolower(*ptr);
    }

    return x % N;
}


// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Open Dictionary File
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        fprintf(stderr, "Could not open dictionary.\n");
        return false;
    }

    // A String To Store Each Word Loaded From The Dictionary
    char dict_word[LENGTH + 1];

    // Read Words from dict one at a time
    while (fscanf(dict, "%s", dict_word) != EOF)
    {
        // Create a new node for each word
        node *n = calloc(1, sizeof(node));

        // Check if the node points to NULL
        if (n == NULL)
        {
            // fprintf(stderr, "Node points to NULL.\n");
            return false;
        }

        // Copy the word into the node
        strcpy(n->word, dict_word);

        // Hash word to obtain a hash value
        int index = hash(dict_word);

        // Insert node into hash table at that loction //
        //// Make this node point to the first node at this location
        n->next = table[index];
        //// Make Table Point To the New Node
        table[index] = n;
        
        // Increment the word count
        WORD_COUNT++;
    }

    // Close the dictionary file when complete
    fclose(dict);
    
    // If We Make It This Far, The Dictionary Was Loaded Correctly.
    return true;
}


// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return WORD_COUNT;
}


// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // For each element in the hash table
    for (int i = 0; i < N; i++)
    {

        // Create two temporary pointers to iterate down the list
        node *cursor = table[i];
        node *tmp = table[i];

        // Iterate down the full length of the linked list
        while (cursor != NULL)
        {
            // Move the cursor to the next node
            cursor = cursor->next;
            
            // Free the previous node
            free(tmp);
            
            // Move temp to catch up with cursor
            tmp = cursor;
        }
    
    }
    return true;
}
