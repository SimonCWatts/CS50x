// Design and implement a program, readability, that computes the Coleman-Liau index of the text.

// Implement your program in a file called readability.c in a directory called readability.

// Your program must prompt the user for a string of text (using get_string).

// Your program should count the number of letters, words, and sentences in the text.

// You may assume that a letter is any lowercase character from a to z or any uppercase character from A to Z,
// any sequence of characters separated by spaces should count as a word, and that any occurrence of a period,
// exclamation point, or question mark indicates the end of a sentence.

// Your program should print as output "Grade X" where X is the grade level computed by the Coleman-Liau formula,
// rounded to the nearest integer.

// If the resulting index number is 16 or higher (equivalent to or greater than a senior undergraduate reading level),
// your program should output "Grade 16+" instead of giving the exact index number.

// If the index number is less than 1, your program should output "Before Grade 1".

// IMPORT LIBRARIES //
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

// DECLARE FUNCTIONS //
string getText(void);
int numLetters(string);
int numWords(string);
int numSentences(string);
int textAge(float, float, float);

////////////////////////////
int main(void)
{
    // Prompt the user for input text
    string text = get_string("Text:");

    // Parse the number of letters, words & sentences
    int length = strlen(text);
    int letters = numLetters(text);
    int words = numWords(text);
    int sentences = numSentences(text);
    
    // Compute the reading age of the text
    int age = textAge(letters, words, sentences);

    // print the age grade per requirements
    if (age < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (age >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", age);
    }
}
/////////////////////////////
int numLetters(string text)
{
    int length = strlen(text);
    int letters = 0;
    for (int i = 0; i <= length; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
    }
    return (letters);
}
/////////////////////////////
int numWords(string text)
{
    int length = strlen(text);
    int words = 0;
    for (int i = 0; i <= length; i++)
    {
        if (isspace(text[i]))
        {
            words++;
        }
    }
    // Plus one because the final word will not have a space after it.
    words++;
    return (words);

}
//////////////////////////////////
int numSentences(string text)
{
    int length = strlen(text);
    int sentences = 0;
    for (int i = 0; i <= length; i++)
    {
        // Check if the character is a '.' or '!' or '?'
        if (text[i] == 33 || text[i] == 46 || text[i] == 63)
        {
            sentences++;
        }
    }
    return (sentences);
}
//////////////////////////////////////////////////
int textAge(float letters, float words, float sentences)
{
    float L = letters / words * 100;   // the average number of letters per 100 words in the text,
    float S = sentences / words * 100; // the average number of sentences per 100 words in the text

    float index = 0.0588 * L - 0.296 * S - 15.8;

    int age = round(index);

    return (age);
}