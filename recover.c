#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE; // creates a new type to store a byte of data... ie...///


int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 2)
    {
        printf("Usage:./recover image\n");
        return 1;
    }

    // Open Input File
    FILE *card = fopen(argv[1], "r");

    // Ensure card was opened correctly.
    if (card == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 1;
    }

    // Counter for the number of JPEGs found.
    int JPGcount = 0;
    
    // Allocate 8 bytes for the JPG Name
    char *img_name = malloc(8);

    // Place holder for the image pointer.
    FILE *img_ptr = NULL;

    // Allocate 512 bytes of memory to store data to search through
    BYTE *buffer = malloc((512 * sizeof(BYTE)));

    // Check the pointer is not NULL
    if (buffer == NULL)
    {
        return 1;
    }

    // Repeatedly read from the card and store in 'buffer' until we get to the end of 'card'
    while (fread(buffer, sizeof(BYTE), 512, card) != 0)
    {
        // If this is the start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If this is the first JPEG
            if (JPGcount == 0)
            {
                // Name the JPEG file with a three digit integer 000.jpeg
                sprintf(img_name, "%03i.jpg", JPGcount);
                
                // Increment the JPG count
                JPGcount++;
    
                // Open a new JPEG file
                img_ptr = fopen(img_name, "w");
    
                // Write 512 bytes
                fwrite(buffer, sizeof(BYTE), 512, img_ptr);
            }
            // If this is not the first JPEG
            else
            {
                // Close the old JPEG
                fclose(img_ptr);
                
                // Name the JPEG file with a three digit integer ###.jpeg
                sprintf(img_name, "%03i.jpg", JPGcount);
                
                // Increment the JPEG count
                JPGcount++;
    
                // Open a new JPEG file
                img_ptr = fopen(img_name, "w");
    
                // Write 512 bytes
                fwrite(buffer, sizeof(BYTE), 512, img_ptr);
            }
        }
        // If this block is NOT the start of new JPEG
        else
        {                
            // If we are already writing to a JPEG file
            if (JPGcount > 0)
            {
                // Keep writing to the same file
                fwrite(buffer, sizeof(BYTE), 512, img_ptr);
            }
        }
    }

    // Free memory for buffer
    free(buffer);

    // Close the imported file
    fclose(card);

    return 0;
}