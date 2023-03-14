#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string text = get_string("Text: ");

    int letters = 0, sentences = 0, words = 1, text_len = strlen(text);
    for (int i = 0; i < text_len; i++)
    {
        text[i] = tolower(text[i]);
        if (text[i] >= 'a' && text[i] <= 'z')
        {
            letters = letters + 1;
        }
        else if (text[i] == '!' || text[i] == '?' || text[i] == '.')
        {
            sentences = sentences + 1;
        }
        else if (text[i] == ' ')
        {
            words = words + 1;
        }
    }

    // L: Average number of letters per 100 words
    // S: Average number of sentences per 100 words
    float L = letters * 100, S = sentences * 100;
    L = L / words;
    S = S / words;

    float grade = 0.0588 * L - 0.296 * S - 15.8;

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %.0f\n", round(grade));
    }
}