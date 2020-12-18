def find_answer_1(input):
    for x in input:
        for y in input:
            sum = x + y
            if sum == 2020:
                return x * y


def find_answer_2(input):
    for x in input:
        for y in input:
            for z in input:
                sum = x + y + z
                if sum == 2020:
                    return x * y * z


if __name__ == "__main__":
    with open("day01.txt") as f:
        input = [int(x) for x in f.readlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
