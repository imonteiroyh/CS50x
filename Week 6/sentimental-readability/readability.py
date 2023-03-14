def get_text():
    text = input('Text: ')
    return text
    

def get_text_parameters(text):
    letters = 0
    sentences = 0
    words = 1

    text = text.lower()
    for i in range(len(text)):
        if text[i] >= 'a' and text[i] <= 'z':
            letters += 1

        elif text[i] == '!' or text[i] == '?' or text[i] == '.':
            sentences += 1

        elif text[i] == ' ':
            words += 1

    text_parameters = {'letters': letters, 'sentences': sentences, 'words': words}
    return text_parameters


def print_grading(text_parameters):
    words = text_parameters['words']
    L = (text_parameters['letters'] * 100) / words
    S = (text_parameters['sentences'] * 100) / words

    grade = 0.0588 * L - 0.296 * S - 15.8

    if grade < 1:
        print('Before Grade 1')

    elif grade > 16:
        print('Grade 16+')

    else:
        print(f'Grade {round(grade)}')


def main():
    text = get_text()
    text_parameters = get_text_parameters(text)
    print_grading(text_parameters)


main()