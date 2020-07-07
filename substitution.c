//// IMPORT LIBRARIES /////
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>


//// DECLARE HELPER FUNCTIONS ////
int validateKey(int, string[]);
int shift(char[], char[]);

///////////// MAIN ////////////////
int main(int argc, string argv[])
{
    string key = argv[1];

    // check key is valid
    if (validateKey(argc, argv) == 1)
    {
        return 1;
    }

    // ask user for plaintext
    string plain_text = get_string("plaintext: ");

    printf("ciphertext: ");

    // convert to ciphertext & print
    shift(plain_text, key);
    return 0;
}

////////// ENCRYPT & PRINT TEXT ////////////
int shift(string plain_text, char key[])
{
    int text_length = strlen(plain_text);

    for (int i = 0; i < text_length; i++)
    {
        if (isupper(plain_text[i]))
        {
            printf("%c", toupper(key[plain_text[i] - 'A']));
        }
        else if (islower(plain_text[i]))
        {
            printf("%c", key[plain_text[i] - 'a']);
        }
        else
        {
            printf("%c", plain_text[i]);
        }
    }
    printf("\n");
    return 0;
}

/////// CHECK USER INPUTS ARE VALID ///////
int validateKey(int num, string user_inputs[])
{
    // check the user provided only one argument
    if (num != 2)
    {
        printf("ERROR: Please Provide ONE Arguement Only!\n");
        return 1;
    }

    string key = user_inputs[1];
    int key_length = strlen(key);

    // check the key has 26 characters
    if (key_length != 26)
    {
        printf("ERROR: Key must contain 26 characters.\nYour key has %i.\n", key_length);
        return 1;
    }

    // iterate over each letter of the key
    for (int i = 0; i < key_length; i++)
    {
        // check each character is a letter
        if (isalpha(key[i]) == false)
        {
            printf("ERROR: Only Provide Letters.\n");
            return 1;
        }

        // check if each value is unique by comparing it to every value (excluding itself) in a duplicate string.
        string key_copy = key;
        for (int k = 0; k < key_length; k++)
        {
            if (key[i] == key_copy[k] && i != k)
            {
                printf("ERROR: Key Should Not Contain Repeated Characters.\n");
                return 1;
            }
        }

        // since the key should be agnostic to upper or lower case we covert all characters to lowercase
        key[i] = tolower(key[i]);
    }

    // update the valid key which also updates it in MAIN
    user_inputs[1] = key;
    return 0;
}