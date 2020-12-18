from functools import reduce


class Adapters:
    cache = {0: 1}

    def __init__(self, list):
        self.list = sorted([0, *input, max(input) + 3])

    def count_all_valid_combinations(self):
        return self.count_all_valid_combinations_for(max(self.list))

    def count_all_valid_combinations_for(self, joltage):
        cached_value = self.cache.get(joltage)
        if cached_value:
            return cached_value

        possible_joltage_below = list(
            filter(lambda x: joltage - 3 <= x < joltage, self.list)
        )

        count = reduce(
            lambda a, v: a + self.count_all_valid_combinations_for(v),
            possible_joltage_below,
            0,
        )
        self.cache[joltage] = count
        return count


def find_answer_1(input):
    adapters = sorted([0, *input, max(input) + 3])

    diff_of_1 = 0
    diff_of_3 = 0

    for i, x in enumerate(adapters):
        if i == 0:
            continue

        diff = x - adapters[i - 1]

        if diff == 1:
            diff_of_1 += 1
        if diff == 3:
            diff_of_3 += 1

    return diff_of_1 * diff_of_3


def find_answer_2(input):
    adapters = Adapters(input)
    return adapters.count_all_valid_combinations()


if __name__ == "__main__":
    with open("day10.txt") as f:
        input = [int(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
