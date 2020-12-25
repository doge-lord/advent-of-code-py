def transform_subject_number(subject_number: int, value: int):
    new_value = value * subject_number
    return new_value % 20201227


def transform_subject_number_with_loop_size(subject_number: int, loop_size: int):
    value = 1

    for _ in range(0, loop_size):
        value = transform_subject_number(subject_number, value)

    return value

    new_subject_number = subject_number
    for value in range(1, loop_size):
        print(value)
        new_subject_number = transform_subject_number(new_subject_number, value)

    return new_subject_number


def get_loop_size(public_key: int):
    value = 1
    loop_size = 0

    while not value == public_key:
        value = transform_subject_number(7, value)
        loop_size += 1

    return loop_size


def find_answer_1(input):
    [door_public_key, card_public_key] = input

    door_loop_size = get_loop_size(door_public_key)
    card_loop_size = get_loop_size(card_public_key)

    encryption_key_1 = transform_subject_number_with_loop_size(
        door_public_key, card_loop_size
    )
    encryption_key_2 = transform_subject_number_with_loop_size(
        card_public_key, door_loop_size
    )

    if encryption_key_1 == encryption_key_2:
        return encryption_key_1


def find_answer_2(input):
    return "ggez"


if __name__ == "__main__":
    with open("day25.txt") as f:
        input = [int(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
