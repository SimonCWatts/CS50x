#include <stdio.h>
#include <cs50.h>
#include <math.h>

int checksum(long card);
string cardtype(long card);


int main(void)
{
    // prompt user for input
    long card = get_long("What's your card number?: ");
    
    // perform checksum
    if (checksum(card) == 0)
    {
        printf("INVALID\n");
        return (0);
    }
    
    // determine what card type
    string x = cardtype(card);
    printf("%s\n", x);
}




string cardtype(long card)
{
    // American Express uses 15-digit numbers,
    // All American Express numbers start with 34 or 37

    // MasterCard uses 16-digit numbers, and
    // Most MasterCard numbers start with 51, 52, 53, 54, or 55

    // Visa uses 13- and 16-digit numbers
    // All Visa numbers start with 4.

    long card_copy = card;

    // determine card length
    int len = 0;
    while (card_copy != 0)
    {
        card_copy /= 10;
        len ++;
    }

    // extract each digit from the card
    card_copy = card;

    int a = card_copy % 10;
    card_copy /= 10;
    int a2 = card_copy % 10;
    card_copy /= 10;
    int b = card_copy % 10;
    card_copy /= 10;
    int b2 = card_copy % 10;
    card_copy /= 10;
    int c = card_copy % 10;
    card_copy /= 10;
    int c2 = card_copy % 10;
    card_copy /= 10;
    int d = card_copy % 10;
    card_copy /= 10;
    int d2 = card_copy % 10;
    card_copy /= 10;
    int e = card_copy % 10;
    card_copy /= 10;
    int e2 = card_copy % 10;
    card_copy /= 10;
    int f = card_copy % 10;
    card_copy /= 10;
    int f2 = card_copy % 10;
    card_copy /= 10;
    int g = card_copy % 10;
    card_copy /= 10;
    int g2 = card_copy % 10;
    card_copy /= 10;
    int h = card_copy % 10;
    card_copy /= 10;
    int h2 = card_copy % 10;


    if (len == 15 && h == 3 && (g2 == 4 || g2 == 7))
    {
        return ("AMEX");
    }
    if (len == 13 && g == 4)
    {
        return ("VISA");
    }
    if (len == 16 && h2 == 4)
    {
        return ("VISA");
    }
    if (len == 16 && h2 == 5 && (h == 1 || h == 2 || h == 3 || h == 4 || h == 5))
    {
        return ("MASTERCARD");
    }
    return ("INVALID");
}

//////////////////////////////////////////////////////////////////////////////////

int checksum(long card)
{
    long card_copy = card;

    // extract each digit from the card
    int a = card_copy % 10;
    card_copy /= 10;
    int a2 = card_copy % 10 * 2;
    card_copy /= 10;
    int b = card_copy % 10;
    card_copy /= 10;
    int b2 = card_copy % 10 * 2;
    card_copy /= 10;
    int c = card_copy % 10;
    card_copy /= 10;
    int c2 = card_copy % 10 * 2;
    card_copy /= 10;
    int d = card_copy % 10;
    card_copy /= 10;
    int d2 = card_copy % 10 * 2;
    card_copy /= 10;
    int e = card_copy % 10;
    card_copy /= 10;
    int e2 = card_copy % 10 * 2;
    card_copy /= 10;
    int f = card_copy % 10;
    card_copy /= 10;
    int f2 = card_copy % 10 * 2;
    card_copy /= 10;
    int g = card_copy % 10;
    card_copy /= 10;
    int g2 = card_copy % 10 * 2;
    card_copy /= 10;
    int h = card_copy % 10;
    card_copy /= 10;
    int h2 = card_copy % 10 * 2;

    int sum = 0;
    // sum the digits of the doubled numbers
    sum += a2 % 10;
    a2 /= 10;
    sum += a2 % 10;

    sum += b2 % 10;
    b2 /= 10;
    sum += b2 % 10;

    sum += c2 % 10;
    c2 /= 10;
    sum += c2 % 10;

    sum += d2 % 10;
    d2 /= 10;
    sum += d2 % 10;

    sum += e2 % 10;
    e2 /= 10;
    sum += e2 % 10;

    sum += f2 % 10;
    f2 /= 10;
    sum += f2 % 10;

    sum += g2 % 10;
    g2 /= 10;
    sum += g2 % 10;

    sum += h2 % 10;
    h2 /= 10;
    sum += h2 % 10;

    // sum the digits of the other numbers
    sum += a;
    sum += b;
    sum += c;
    sum += d;
    sum += e;
    sum += f;
    sum += g;
    sum += h;

    // check if it is a valid card
    if (sum % 10 == 0)
    {
        return (1);
    }

    // if the card is valid return TRUE
    return (0);
}