def tally_trees(input, right, down):
    CHAR_TREE = "#"
    current_row = 0
    current_col = 0
    tree_counter = 0

    for x in input:
        if current_row % down == 0:
            if x[current_col] == CHAR_TREE:
                tree_counter += 1

            current_col += right

            if current_col >= len(x):
                current_col -= len(x)

        current_row += 1

    return tree_counter


def find_answer_1(input):
    return tally_trees(input, 3, 1)


def find_answer_2(input):
    return (
        tally_trees(input, 1, 1)
        * tally_trees(input, 3, 1)
        * tally_trees(input, 5, 1)
        * tally_trees(input, 7, 1)
        * tally_trees(input, 1, 2)
    )


if __name__ == "__main__":
    with open("day03.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
