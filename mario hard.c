// Prints an n-by-n grid of bricks with a loop

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // ask the user for an integer between 1-8 inclusive
    int n = get_int("How Many Steps: ");
    while (n < 1 || n > 8)
    {
        n = get_int("How Many Steps: ");
    }

    // construct a prymid n x n
    // i counts each line
    for (int i = 0; i < n; i++)
    {
        // k counts the number of spaces spaces
        for (int k = 1; k < n - i; k++)
        {
            printf(" ");
        }

        // j counts the number of hashes
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }
        
        // add a double space
        printf("  ");
        
        // j counts the number of hashes
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // new line
        printf("\n");
    }
}
