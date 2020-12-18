def decode_bits(input):
    bit_coversion = {"F": "0", "L": "0", "B": "1", "R": "1"}
    bits = input.translate(str.maketrans(bit_coversion))
    length = len(bits)

    min = 0
    max = (2 ** length) - 1

    for x in range(length):
        removed = 2 ** (length - 1 - x)
        if int(bits[x]):
            min += removed
        else:
            max -= removed

    # Assuming min and max are already equal at this point
    return min


def get_seat_number(input):
    row = decode_bits(input[0:7])
    col = decode_bits(input[7:10])

    return (row * 8) + col


def find_answer_1(input):
    return max(list(map(lambda x: get_seat_number(x), input)))


def find_answer_2(input):
    occupied_seat_ids = list(map(lambda x: get_seat_number(x), input))
    highest_seat_id = max(occupied_seat_ids)
    available_seat_ids = list(
        filter(lambda x: not x in occupied_seat_ids, range(highest_seat_id + 1))
    )
    valid_seat_ids = list(
        filter(
            lambda x: not (
                (x + 1) in available_seat_ids or (x - 1) in available_seat_ids
            ),
            available_seat_ids,
        )
    )

    return valid_seat_ids


if __name__ == "__main__":
    with open("day05.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
