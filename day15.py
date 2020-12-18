def find_value_at_index(numbers, instance):
    count = len(input) - 1
    used_numbers = {}
    last_number = numbers[-1]

    for i, n in enumerate(numbers[0 : len(numbers) - 1]):
        used_numbers[n] = i

    while count < (instance - 1):
        try:
            last_index = used_numbers[last_number]
            used_numbers[last_number] = count
            age = count - last_index
            last_number = age
        except:
            used_numbers[last_number] = count
            last_number = 0

        count += 1

    return last_number


def find_answer_1(input):
    return find_value_at_index(list(input), 2020)


def find_answer_2(input):
    return find_value_at_index(list(input), 30000000)


if __name__ == "__main__":
    with open("day15.txt") as f:
        input = [int(x) for x in f.read().split(",")]

    print(find_answer_1(input))
    print(find_answer_2(input))
