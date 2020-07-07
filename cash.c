#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // this is the answer
    int quarters = 0;
    int dimes = 0;
    int nickels = 0;
    int cents = 0;

    // prompt user for input that is non-negative
    float dollars  = get_float("How Much Change:\n");
    while (dollars < 0)
    {
        dollars  = get_float("How Much Change:\n");
    }
    
    // convert to int to avoid rounding errors
    int change = round(dollars * 100);
    
    // decrement .25c until negative or zero
    quarters = change / 25;
    change = change % 25;
    // decrement by 0.1c until negative or zero
    dimes = change / 10;
    change = change % 10;
    // decrement by 0.05c until negative or zero
    nickels = change / 5;
    change = change % 5;
    // decrement by 0.01c until negatives or zero
    cents = change;

    printf("%i\n", quarters + dimes + nickels + cents);
}