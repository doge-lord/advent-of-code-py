from functools import reduce


def find_answer_1(input):
    return reduce(
        lambda acc, val: acc + len(set("".join(val))),
        input,
        0,
    )


def find_answer_2(input):
    return reduce(
        lambda acc, val: acc
        + len(
            reduce(
                lambda a, v: a.intersection(v),
                val,
                set("".join(val)),
            )
        ),
        input,
        0,
    )


if __name__ == "__main__":
    with open("day06.txt") as f:
        input = [str(x).split("\n") for x in f.read().split("\n\n")]

    print(find_answer_1(input))
    print(find_answer_2(input))
