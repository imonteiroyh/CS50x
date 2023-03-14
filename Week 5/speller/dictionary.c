// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <math.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26 * 26 * 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_value = hash(word);

    if (table[hash_value] == NULL)
    {
        return false;
    }

    node *pointer = table[hash_value];
    while (pointer != NULL)
    {
        if (strcasecmp(pointer->word, word) == 0)
        {
            return true;
        }

        pointer = pointer->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    int len_to_hash;
    if (strlen(word) < 3)
    {
        len_to_hash = strlen(word);
    }
    else
    {
        len_to_hash = 3;
    }

    int hash_value = 0;
    for (int i = 0; i < len_to_hash; i++)
    {

        hash_value = hash_value + pow(26, (len_to_hash - 1) - i) * (toupper(word[i]) - 'A');
    }

    return hash_value;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char current_word[LENGTH + 1];
    int hash_value;

    while (fscanf(file, "%s", current_word) == 1)
    {
        node *dictionary_node = malloc(sizeof(node));
        if (dictionary_node == NULL)
        {
            unload();
            return false;
        }

        strcpy(dictionary_node->word, current_word);
        dictionary_node->next = NULL;

        hash_value = hash(current_word);
        if (table[hash_value] != NULL)
        {
            dictionary_node->next = table[hash_value];
        }
        table[hash_value] = dictionary_node;
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    int dictionary_size = 0;

    for (int i = 0; i < N; i++)
    {
        if (table[i] != NULL)
        {
            node *pointer = table[i];
            while (pointer != NULL)
            {
                dictionary_size = dictionary_size + 1;
                pointer = pointer->next;
            }
        }
    }

    return dictionary_size;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *pointer = table[i];
        while (pointer != NULL)
        {
            node *next_node = pointer->next;
            free(pointer);
            pointer = next_node;
        }
    }

    return true;
}
