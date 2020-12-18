from functools import reduce
import re

MASK = "mask"
MEM = "mem"


def parse_input(input):
    program = []

    for line in input:
        match = re.match(r"mask\s=\s([0-1X]+)", line)
        if match:
            program.append({"type": MASK, "value": match.group(1)})
            continue

        match = re.match(r"mem\[(\d+)\]\s=\s(\d+)", line)
        if match:
            program.append(
                {
                    "type": MEM,
                    "address": int(match.group(1)),
                    "value": int(match.group(2)),
                }
            )
            continue

    return program


def apply_mask(value: int, mask: str):
    value_in_bin = bin(value)[2:].rjust(len(mask), "0")
    new_value = ""

    for i, mask_bit in enumerate(mask):
        if mask_bit == "X":
            new_value += value_in_bin[i]
        else:
            new_value += mask_bit

    return int(new_value, 2)


def apply_mask_v2(address: int, mask: str):
    value_in_bin = bin(address)[2:].rjust(len(mask), "0")
    masked_address = ""

    for i, mask_bit in enumerate(mask):
        if mask_bit == "X":
            masked_address += "X"
        elif mask_bit == "0":
            masked_address += value_in_bin[i]
        elif mask_bit == "1":
            masked_address += mask_bit

    masked_bit_count = reduce(lambda a, v: a + 1 if v == "X" else a, masked_address, 0)
    addresses = []

    for i in range(0, 2 ** masked_bit_count):
        new_address = masked_address

        for x in bin(i)[2:].rjust(masked_bit_count, "0"):
            new_address = new_address.replace("X", x, 1)
        else:
            addresses.append(int(new_address, 2))

    return addresses


def execute_program(program):
    memory = {}
    current_mask = None

    for line in program:
        if line["type"] == MASK:
            current_mask = line["value"]
        elif line["type"] == MEM:
            memory[line["address"]] = apply_mask(line["value"], current_mask)

    return memory


def execute_program_v2(program):
    memory = {}
    current_mask = None

    for line in program:
        if line["type"] == MASK:
            current_mask = line["value"]
        elif line["type"] == MEM:
            for address in apply_mask_v2(line["address"], current_mask):
                memory[address] = line["value"]

    return memory


def find_answer_1(input):
    program = parse_input(input)
    memory = execute_program(program)

    return reduce(lambda a, v: a + v, memory.values(), 0)


def find_answer_2(input):
    program = parse_input(input)
    memory = execute_program_v2(program)

    return reduce(lambda a, v: a + v, memory.values(), 0)


if __name__ == "__main__":
    with open("day14.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
