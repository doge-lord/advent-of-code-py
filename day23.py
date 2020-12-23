def build_linked_list(initial_cups, cup_count):
    linked_list = {}
    cups = [*initial_cups, *range(len(initial_cups) + 1, cup_count + 1)]

    for i, cup in enumerate(cups):
        if cup_count > i + 1:
            linked_list[cup] = cups[i + 1]
        else:
            linked_list[cup] = initial_cups[0]

    return linked_list


def find_answer_1(input):
    cups = list(input)
    current_cup_index = -1

    number_of_moves = 100
    counter = 0

    while counter < number_of_moves:
        current_cup_index = (current_cup_index + 1) % len(input)
        current_cup = cups[current_cup_index]

        # Pick up cups
        pick_up = cups[current_cup_index + 1 : current_cup_index + 4]
        if len(pick_up) < 3:
            pick_up.extend(cups[: 3 - len(pick_up)])

        # Remove picked cups
        for cup in pick_up:
            cups.remove(cup)

        destination_cup = current_cup - 1
        if destination_cup < min(input):
            destination_cup = max(input)

        while destination_cup in pick_up:
            destination_cup -= 1

            if destination_cup < min(input):
                destination_cup = max(input)

        place_to = cups.index(destination_cup) + 1
        cups = cups[:place_to] + pick_up + cups[place_to:]

        # Rearrange cups
        while not cups.index(current_cup) == current_cup_index:
            cups.append(cups.pop(0))

        counter += 1

    # Rearrange final cup order
    cups = cups[cups.index(1) + 1 :] + cups[: cups.index(1)]

    return int("".join(map(str, cups)))


def find_answer_2(input):
    # This solution can also be used to solve part 1
    min_cup = 1
    max_cup = 1000000
    number_of_moves = 10000000

    linked_list = build_linked_list(input, max_cup)
    current_cup = input[0]

    counter = 0

    while counter < number_of_moves:
        pick_up = [
            linked_list[current_cup],
            linked_list[linked_list[current_cup]],
            linked_list[linked_list[linked_list[current_cup]]],
        ]

        destination_cup = current_cup - 1 if min_cup <= current_cup - 1 else max_cup
        while destination_cup in pick_up:
            destination_cup -= 1

            if destination_cup < min_cup:
                destination_cup = max_cup

        after_destination_cup = linked_list[destination_cup]
        linked_list[destination_cup] = pick_up[0]
        linked_list[current_cup] = linked_list[pick_up[2]]
        linked_list[pick_up[2]] = after_destination_cup

        current_cup = linked_list[current_cup]

        counter += 1

    return linked_list[1] * linked_list[linked_list[1]]


if __name__ == "__main__":
    with open("day23.txt") as f:
        input = [int(x) for x in list(f.read())]

    print(find_answer_1(input))
    print(find_answer_2(input))
