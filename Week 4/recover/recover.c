#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef uint8_t BYTE;

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    char *infile = argv[1];

    FILE *raw = fopen(infile, "r");
    if (raw == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 1;
    }

    int file_counter = 0, reading = 0;
    char filename[10];

    BYTE buffer[BLOCK_SIZE];
    FILE *image = NULL;

    while (fread(buffer, 1, BLOCK_SIZE, raw) == BLOCK_SIZE)
    {
        // Check the first four bytes
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (image != NULL)
            {
                fclose(image);
            }

            sprintf(filename, "%03i.jpg", file_counter);
            image = fopen(filename, "w");
            if (image == NULL)
            {
                fclose(raw);
                printf("Could not create %s.\n", filename);
                return 1;
            }

            reading = 1;
            file_counter += 1;
        }

        if (reading == 1)
        {
            fwrite(buffer, 1, BLOCK_SIZE, image);
        }
    }

    fclose(image);
    fclose(raw);
}