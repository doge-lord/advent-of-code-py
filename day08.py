class Operation:
    ACC = "acc"
    JMP = "jmp"
    NOP = "nop"


def parse_line(line):
    [op, value] = line.split(" ")
    return (op, int(value))


def parse_input(input):
    return list(map(lambda x: parse_line(x), input))


def run_program(program):
    accumulator = 0

    current_line = 0
    lines_ran = []

    while not (current_line in lines_ran or current_line >= len(program)):
        (op, value) = program[current_line]
        lines_ran.append(current_line)

        if op == Operation.ACC:
            accumulator += value
            current_line += 1
        elif op == Operation.JMP:
            current_line += value
        elif op == Operation.NOP:
            current_line += 1

    return (current_line, accumulator)


def find_answer_1(input):
    program = parse_input(input)
    (_, accumulator) = run_program(program)
    return accumulator


def find_answer_2(input):
    program = parse_input(input)

    for i, (op, _) in enumerate(program):
        if op == Operation.JMP:
            program_copy = parse_input(input)
            program_copy[i] = (Operation.NOP, program_copy[i][1])
            (current_line, accumulator) = run_program(program_copy)

            if current_line == len(program_copy):
                return accumulator

        elif op == Operation.NOP:
            program_copy = parse_input(input)
            program_copy[i] = (Operation.JMP, program_copy[i][1])
            (current_line, accumulator) = run_program(program_copy)

            if current_line == len(program_copy):
                return accumulator


if __name__ == "__main__":
    with open("day08.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
