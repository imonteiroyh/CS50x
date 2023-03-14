#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height = -1;

    // Verifica se a altura está entre 1 e 8
    while (height < 1 || height > 8)
    {
        height = get_int("Height: ");
    }

    // Cada linha da pirâmide
    for (int i = 1; i <= height; i += 1)
    {
        // Pirâmide esquerda (espaços)
        for (int j = 0; j < height - i; j += 1)
        {
            printf(" ");
        }

        // Pirâmide esquerda (hashes)
        for (int j = 0; j < i; j += 1)
        {
            printf("#");
        }

        // Espaço
        for (int j = 0; j < 2; j += 1)
        {
            printf(" ");
        }

        // Pirâmide direita (hashes)
        for (int j = 0; j < i; j += 1)
        {
            printf("#");
        }

        printf("\n");
    }
}