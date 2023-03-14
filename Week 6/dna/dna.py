import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit('Usage: python dna.py data.csv sequence.txt')

    # TODO: Read database file into a variable
    persons = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            persons.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], 'r') as file:
        dna = file.readline()

    # TODO: Find longest match of each STR in DNA sequence
    dna_str = list(persons[0].keys())
    dna_str.pop(0)

    count = {}
    for str in dna_str:
        current_longest_match = longest_match(dna, str)
        count[str] = current_longest_match

    # TODO: Check database for matching profiles
    match = check_match(persons, count, dna_str)
    print(match)


def check_match(persons, count, dna_str):
    for person in persons:
        matches = 0

        for str in dna_str:
            if int(person[str]) == count[str]:
                matches += 1

        if matches == len(dna_str):
            return person['name']

    return 'No match'


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
