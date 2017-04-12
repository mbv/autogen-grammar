from sys import argv, stderr
from generator import *


def read_grammar(file_name):
    result = None
    with open(file_name, 'r') as input_file:
        sequences = [s.rstrip() for s in input_file.readlines()]
        if len(sequences) > 1:
            result = sequences

    return result


def main():
    sequences = read_grammar(argv[1])
    if sequences:
        AutoGenerateText(sequences).run()
    else:
        print('Invalid input', file=stderr)


if __name__ == '__main__':
    main()
