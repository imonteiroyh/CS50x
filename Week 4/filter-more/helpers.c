#include "helpers.h"
#include <math.h>
#include <stdlib.h>

typedef struct
{
    int blue;
    int green;
    int red;
} SOBELG;

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int blue_value = image[i][j].rgbtBlue;
            int green_value = image[i][j].rgbtGreen;
            int red_value = image[i][j].rgbtRed;

            int gray_value = round((float)(blue_value + green_value + red_value) / 3);


            image[i][j].rgbtBlue = gray_value;
            image[i][j].rgbtGreen = gray_value;
            image[i][j].rgbtRed = gray_value;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (int) width / 2; j++)
        {
            RGBTRIPLE tmp = image[i][(width - 1) - j];
            image[i][(width - 1) - j] = image[i][j];
            image[i][j] = tmp;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE(*auxiliar_image)[width] = calloc(height, width * sizeof(RGBTRIPLE));
    int mean_blue_value, mean_green_value, mean_red_value, total_blocks;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            auxiliar_image[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            mean_blue_value = 0;
            mean_green_value = 0;
            mean_red_value = 0;

            total_blocks = 0;
            for (int k = i - 1; k <= i + 1; k++)
            {
                if (k >= 0 && k <= height - 1)
                {
                    for (int l = j - 1; l <= j + 1; l++)
                    {
                        if (l >= 0 && l <= width - 1)
                        {
                            mean_blue_value += auxiliar_image[k][l].rgbtBlue;
                            mean_green_value += auxiliar_image[k][l].rgbtGreen;
                            mean_red_value += auxiliar_image[k][l].rgbtRed;
                            total_blocks += 1;
                        }
                    }
                }

            }

            mean_blue_value = round((float) mean_blue_value / total_blocks);
            mean_green_value = round((float) mean_green_value / total_blocks);
            mean_red_value = round((float) mean_red_value / total_blocks);

            image[i][j].rgbtBlue = mean_blue_value;
            image[i][j].rgbtGreen = mean_green_value;
            image[i][j].rgbtRed = mean_red_value;
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    SOBELG gx[height][width], gy[height][width];

    int gxm[] = {-1, 0, 1, -2, 0, 2, -1, 0, 1};
    int gym[] = {-1, -2, -1, 0, 0, 0, 1, 2, 1};
    int current;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            gx[i][j].blue = 0;
            gx[i][j].green = 0;
            gx[i][j].red = 0;

            gy[i][j].blue = 0;
            gy[i][j].green = 0;
            gy[i][j].red = 0;

            current = 0;
            for (int k = i - 1; k <= i + 1; k++)
            {
                if (k >= 0 && k <= height - 1)
                {
                    for (int l = j - 1; l <= j + 1; l++)
                    {
                        if (l >= 0 && l <= width - 1)
                        {
                            gx[i][j].blue += gxm[current] * image[k][l].rgbtBlue;
                            gx[i][j].green += gxm[current] * image[k][l].rgbtGreen;
                            gx[i][j].red += gxm[current] * image[k][l].rgbtRed;

                            gy[i][j].blue += gym[current] * image[k][l].rgbtBlue;
                            gy[i][j].green += gym[current] * image[k][l].rgbtGreen;
                            gy[i][j].red += gym[current] * image[k][l].rgbtRed;

                            current += 1;
                        }
                        else
                        {
                            current += 1;
                        }
                    }
                }
                else
                {
                    current += 3;
                }

            }

        }
    }

    int blue_value, green_value, red_value;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            blue_value = round((float) sqrt((float) pow(gx[i][j].blue, 2) + (float) pow(gy[i][j].blue, 2)));
            green_value = round((float) sqrt((float) pow(gx[i][j].green, 2) + (float) pow(gy[i][j].green, 2)));
            red_value = round((float) sqrt((float) pow(gx[i][j].red, 2) + (float) pow(gy[i][j].red, 2)));

            if (blue_value > 255)
            {
                blue_value = 255;
            }

            if (green_value > 255)
            {
                green_value = 255;
            }

            if (red_value > 255)
            {
                red_value = 255;
            }

            image[i][j].rgbtBlue = blue_value;
            image[i][j].rgbtGreen = green_value;
            image[i][j].rgbtRed = red_value;
        }
    }


    return;
}
