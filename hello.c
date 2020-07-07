#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Prompt user for a name
    string name = get_string("What's your name?\n");
    
    // Say "Hello" to the user
    printf("Hello, %s\n", name);
}