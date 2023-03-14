#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int check_valid(int argc, string argv)
{
    if (argc == 1)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (argc == 2)
    {
        int key_len = strlen(argv);

        if (key_len != 26)
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }

        int check[26];
        memset(check, 0, 26);

        for (int i = 0; i < 26; i++)
        {
            if (check[tolower(argv[i]) - 'a'] == 0)
            {
                check[tolower(argv[i]) - 'a'] = 1;
            }
            else
            {
                printf("Invalid key.\n");
                return 1;
            }
        }
    }
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    return 0;
}

int main(int argc, string argv[])
{
    if (check_valid(argc, argv[1]) == 1)
    {
        return 1;
    }

    string plain_text = get_string("plaintext: ");

    string key = argv[1];
    for (int i = 0; i < 26; i++)
    {
        key[i] = tolower(key[i]);
    }

    string cipher_text = plain_text;
    int text_len = strlen(plain_text);

    for (int i = 0; i < text_len; i++)
    {
        if (isalpha(cipher_text[i]))
        {
            if (isupper(cipher_text[i]))
            {
                cipher_text[i] = toupper(key[tolower(plain_text[i]) - 'a']);
            }
            else
            {
                cipher_text[i] = key[plain_text[i] - 'a'];
            }
        }

    }

    printf("ciphertext: %s\n", cipher_text);
}