#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // loop through each row 'r'
    for (int r = 0; r < height; r++)
    {
        // loop through each column 'c'
        for (int c = 0; c < width; c++)
        {
            // compute average pixel colour to make it grey
            int average = round((image[r][c].rgbtBlue + image[r][c].rgbtGreen + image[r][c].rgbtRed) / 3.0);

            // convert each pixel to grey
            image[r][c].rgbtBlue = average;
            image[r][c].rgbtGreen = average;
            image[r][c].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // loop through each row 'r'
    for (int r = 0; r < height; r++)
    {
        // loop through each column 'c'
        for (int c = 0; c < width; c++)
        {
            // compute sepia pixel colours
            int sepiaRed = round(0.393 * image[r][c].rgbtRed + 0.769 * image[r][c].rgbtGreen + 0.189 * image[r][c].rgbtBlue);
            int sepiaGreen = round(0.349 * image[r][c].rgbtRed + 0.686 * image[r][c].rgbtGreen + 0.168 * image[r][c].rgbtBlue);
            int sepiaBlue = round(0.272 * image[r][c].rgbtRed + 0.534 * image[r][c].rgbtGreen + 0.131 * image[r][c].rgbtBlue);

            // convert red pixel to sepia
            if (sepiaRed > 255)
            {
                image[r][c].rgbtRed = 255;
            }
            else
            {
                image[r][c].rgbtRed = sepiaRed;
            }

            // convert green pixel to sepia
            if (sepiaGreen > 255)
            {
                image[r][c].rgbtGreen = 255;
            }
            else
            {
                image[r][c].rgbtGreen = sepiaGreen;
            }

            // convert blue pixel to sepia
            if (sepiaBlue > 255)
            {
                image[r][c].rgbtBlue = 255;
            }
            else
            {
                image[r][c].rgbtBlue = sepiaBlue;
            }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // make a copy of the image (one pixel at a time)
    RGBTRIPLE image_copy[height][width];
    // loop through each row 'r'
    for (int r = 0; r < height; r++)
    {
        // loop through each column 'c'
        for (int c = 0; c < width; c++)
        {
            // copy each pixel in reverse
            image_copy[r][c].rgbtBlue = image[r][width - 1 - c].rgbtBlue;
            image_copy[r][c].rgbtGreen = image[r][width - 1 - c].rgbtGreen;
            image_copy[r][c].rgbtRed = image[r][width - 1 - c].rgbtRed;
        }

        // loop back through each column 'c' copying the reflection onto the orignial image array
        for (int c = 0; c < width; c++)
        {
            // copy each pixel
            image[r][c].rgbtBlue = image_copy[r][c].rgbtBlue;
            image[r][c].rgbtGreen = image_copy[r][c].rgbtGreen;
            image[r][c].rgbtRed = image_copy[r][c].rgbtRed;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // make a copy of the image (one pixel at a time)
    RGBTRIPLE image_copy[height][width];
    // loop through each row 'r'
    for (int r = 0; r < height; r++)
    {
        // loop through each column 'c'
        for (int c = 0; c < width; c++)
        {
            // copy each pixel
            image_copy[r][c].rgbtBlue = image[r][c].rgbtBlue;
            image_copy[r][c].rgbtGreen = image[r][c].rgbtGreen;
            image_copy[r][c].rgbtRed = image[r][c].rgbtRed;
        }
    }

    //// NOW COPY BLURRED PIXELS BACK INTO THE ORIGINAL IMAGE ARRAY
    // loop through each row 'r'
    for (int r = 0; r < height; r++)
    {
        // loop through each column 'c'
        for (int c = 0; c < width; c++)
        {
            // compute blurred pixel colours
            int blurRed = 0;
            int blurBlue = 0;
            int blurGreen = 0;
            float count = 0.0;

            // i x j is a 3x3 box of pixes surrounding the pixel we want to blur
            for (int i = -1; i < 2; i++)
            {
                for (int j = -1; j < 2; j++)
                {
                    // check if each offset pixel is within the boarders of the image
                    if (r + i >= 0 && r + i < height && c + j >= 0 && c + j < width)
                    {
                        blurRed += image_copy[r + i][c + j].rgbtRed;
                        blurBlue += image_copy[r + i][c + j].rgbtBlue;
                        blurGreen += image_copy[r + i][c + j].rgbtGreen;
                        count++;
                    }
                }
            }

            // compute the blurred average values
            blurRed = round(blurRed / count);
            blurBlue = round(blurBlue / count);
            blurGreen = round(blurGreen / count);

            // update the orginal image array
            image[r][c].rgbtBlue = blurBlue;
            image[r][c].rgbtGreen = blurGreen;
            image[r][c].rgbtRed = blurRed;
        }
    }
    return;
}
