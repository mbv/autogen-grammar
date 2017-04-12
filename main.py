from sys import argv, stderr
from generator import *


def read_grammar(file_name):
    result = None
    with open(file_name, 'r') as input_file:
        lines = [s.rstrip() for s in input_file.readlines()]
        if len(lines) > 1:
            result = lines

    return result


def main():
    lines = read_grammar(argv[1])
    if lines:
        AutoGenerateText().run(lines)
    else:
        print('Invalid input', file=stderr)


if __name__ == '__main__':
    main()
