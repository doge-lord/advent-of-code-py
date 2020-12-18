from functools import reduce
import re


def parse_input(input):
    match = re.search(r"(\d+)\-(\d+)\s([A-Za-z]):\s([A-Za-z]+)", input)
    return (int(match.group(1)), int(match.group(2)), match.group(3), match.group(4))


def tally_valid_passwords_1(acc, value):
    (min, max, required_char, password) = parse_input(value)
    matched_chars_count = len(re.findall(required_char, password))

    if matched_chars_count >= min and matched_chars_count <= max:
        return acc + 1
    else:
        return acc


def tally_valid_passwords_2(acc, value):
    (position_1, position_2, required_char, password) = parse_input(value)

    if (password[position_1 - 1] == required_char) ^ (
        password[position_2 - 1] == required_char
    ):
        return acc + 1
    else:
        return acc


def find_answer_1(input):
    return reduce(tally_valid_passwords_1, input, 0)


def find_answer_2(input):
    return reduce(tally_valid_passwords_2, input, 0)


if __name__ == "__main__":
    with open("day02.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
