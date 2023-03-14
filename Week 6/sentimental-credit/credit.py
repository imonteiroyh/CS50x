def get_card_number():
    while True:
        card_number = input('Number: ')

        if card_number.isnumeric():
            return int(card_number)


def get_card_parameters(card_number):
    sum_normal = 0
    sum_by_2 = 0
    sum_total = 0
    counter = 0

    while card_number > 0:
        counter += 1

        current_last_digit = card_number % 10

        if counter % 2 == 1:
            sum_normal += current_last_digit

        else:
            validator = 2 * current_last_digit
            if validator >= 10:
                sum_by_2 += 1 + (validator % 10)

            else:
                sum_by_2 += validator

        card_number = int(card_number / 10)

    sum_total = sum_normal + sum_by_2

    card_parameters = {'sum_total': sum_total, 'counter': counter}

    return card_parameters


def print_card_type(card_number, card_parameters):
    first_number = str(card_number)[0]
    second_number = str(card_number)[1]

    sum_total = card_parameters['sum_total']
    counter = card_parameters['counter']

    if sum_total % 10 != 0:
        print('INVALID')

    elif counter == 15 and first_number == '3' and (second_number == '3' or second_number == '7'):
        print('AMEX')

    elif counter == 13 or (counter == 16 and first_number == '4'):
        print('VISA')

    elif counter == 16 and first_number == '5' and (second_number >= '1' and second_number <= '5'):
        print('MASTERCARD')

    else:
        print('INVALID')


def main():
    card_number = get_card_number()
    card_parameters = get_card_parameters(card_number)
    print_card_type(card_number, card_parameters)


main()