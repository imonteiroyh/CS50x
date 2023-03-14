#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Número do cartão
    long number = get_long("Number: ");

    // Transformando em string para auxiliar mais tarde
    char card[20];
    sprintf(card, "%li", number);
    int firstNumber = (int) card[0] - 48, secondNumber = (int) card[1] - 48;

    // Verifica validade
    int sumNormal = 0, sumBy2 = 0, sumTotal = 0, counter = 0;

    // Pegar cada dígito a partir do último e somar à variável correspondente
    while (number > 0)
    {
        counter += 1;

        if (counter % 2 == 1)
        {
            sumNormal += number % 10;
        }
        else
        {
            int temp = 2 * (number % 10);
            if (temp >= 10)
            {
                sumBy2 += 1 + (temp % 10);
            }
            else
            {
                sumBy2 += temp;
            }
        }

        number /= 10;
    }

    // Efetuando a soma total
    sumTotal = sumNormal + sumBy2;

    // Verificando se o cartão é válido, se sim, qual seu tipo
    if (sumTotal % 10 != 0)
    {
        printf("INVALID\n");
    }
    else if (counter == 15 && firstNumber == 3 && (secondNumber == 3 || secondNumber == 7))
    {
        printf("AMEX\n");
    }
    else if (counter == 13 || (counter == 16 && card[0] == '4'))
    {
        printf("VISA\n");
    }
    else if (counter == 16 && firstNumber == 5 && (secondNumber >= 1 && secondNumber <= 5))
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }
}