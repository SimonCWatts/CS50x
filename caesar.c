// Specification
// Design and implement a program, caesar, that encrypts messages using Caesar’s cipher.

// Implement your program in a file called caesar.c in a directory called caesar.
// Your program must accept a single command-line argument, a non-negative integer. Let’s call it k for the sake of discussion.
// If your program is executed without any command-line arguments or with more than one command-line argument,
// ... your program should print an error message of your choice (with printf) and return from main a value of 1 (which tends to signify an error) immediately.
// If any of the characters of the command-line argument is not a decimal digit, your program should print the message Usage: ./caesar key and return from main a value of 1.
// Do not assume that k will be less than or equal to 26. Your program should work for all non-negative integral values of k less than 2^31 - 26.
// ... In other words, you don’t need to worry if your program eventually breaks if the user chooses a value for k that’s too big or almost too big to fit in an int.
// ... (Recall that an int can overflow.) But, even if k is greater than 26, alphabetical characters in your program’s input should remain alphabetical characters in your program’s output.
// ... For instance, if k is 27, A should not become [ even though [ is 27 positions away from A in ASCII, per http://www.asciichart.com/[asciichart.com];
// ... A should become B, since B is 27 positions away from A, provided you wrap around from Z to A.
// Your program must output plaintext: (without a newline) and then prompt the user for a string of plaintext (using get_string).
// Your program must output ciphertext: (without a newline) followed by the plaintext’s corresponding ciphertext, with each alphabetical character in the plaintext “rotated” by k positions;
// ... non-alphabetical characters should be outputted unchanged.
// Your program must preserve case: capitalized letters, though rotated, must remain capitalized letters; lowercase letters, though rotated, must remain lowercase letters.
// After outputting ciphertext, you should print a newline. Your program should then exit by returning 0 from main.

//// IMPORT LIBRARIES /////
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>
#include <ctype.h>
#include <stdlib.h>

//// DECLARE HELPER FUNCTIONS ////
int checkKey(int, string);
string getText(void);
string caesar(string, int);


int main(int argc, string argv[])
{
    // check key is valid
    int key = checkKey(argc, *argv);            //// why did I have to use the "*" ??
    if (key == -99)
    {
        return (1);
    }

    // ask user for plaintext
    string plain_text = get_string("plaintext: ");

    // convert to ciphertext
    printf("ciphertext: ");
    string cipher_text = caesar(plain_text, key);
    return (0);
}




//// ENCRYPT TEXT ////
string caesar(string plain_text, int key)
{
    int text_length = strlen(plain_text);
    string cipher_text[text_length];

    for (int i = 0; i < text_length; i++)
    {
        if (isupper(plain_text[i]))
        {
            printf("%c", (plain_text[i] - 'A' + key) % 26 + 'A');
        }
        else if (islower(plain_text[i]))
        {
            printf("%c", (plain_text[i] - 'a' + key) % 26 + 'a');
        }
        else
        {
            printf("%c", plain_text[i]);
        }
    }
    printf("\n");
    return (0);
}








//// CHECK USER INPUTS ARE CORRECT ////
int checkKey(int argc, string argv)
{
    // check the user provided only one additional input
    if (argc != 2)
    {
        printf("PLEASE PROVIDE ONE PARAMETER!\n");
        return (-99);
    }

    // check the input was a positive integer
    string key = &argv[9];                              /// WHY DID I HAVE TO WRITE "&argv[9]" ???
    int key_length = strlen(key);
    for (int i = 0; i < key_length; i++)
    {
        if (isdigit(key[i]) == false)
        {
            printf("Usage: ./caesar key\n");
            return (-99);
        }
    }

    // otherwise input is correct -> return the key as in int
    int int_key = atoi(key);
    return (int_key);

}