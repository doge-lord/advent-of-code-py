from functools import reduce


def find_invalid_number(preamble_len, list):
    for i, x in enumerate(list):
        if i < preamble_len:
            continue

        is_valid = False
        prev_numbers = list[i - preamble_len : i]
        for prev_number_a in prev_numbers:
            for prev_number_b in prev_numbers:
                if prev_number_a == prev_number_b:
                    continue

                if x == prev_number_a + prev_number_b:
                    is_valid = True
                    break

            if is_valid:
                break

        if not is_valid:
            return x


def find_contiguous_set_with_sum(sum, list):
    numbers_before_sum = list[0 : list.index(sum)]

    for start, _ in enumerate(numbers_before_sum):
        for end in [*range(start + 2, len(numbers_before_sum))]:
            contiguous_set = numbers_before_sum[start:end]
            sum_of_contiguous_set = reduce(lambda a, v: a + v, contiguous_set)

            if sum == sum_of_contiguous_set:
                return contiguous_set


def find_answer_1(input):
    return find_invalid_number(25, input)


def find_answer_2(input):
    invalid_number = find_invalid_number(25, input)
    contiguous_set = find_contiguous_set_with_sum(invalid_number, input)

    return min(contiguous_set) + max(contiguous_set)


if __name__ == "__main__":
    with open("day09.txt") as f:
        input = [int(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
