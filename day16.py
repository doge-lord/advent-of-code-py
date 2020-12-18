import re
from functools import reduce


def parse_rule(line):
    match = re.match(r"([a-z\s]+):\s(\d+)-(\d+)\sor\s(\d+)-(\d+)", line)

    if match:
        return {
            "field": match.group(1),
            "ranges": [
                (
                    int(match.group(2)),
                    int(match.group(3)),
                ),
                (
                    int(match.group(4)),
                    int(match.group(5)),
                ),
            ],
        }


def parse_rules(data):
    rules_data = map(lambda line: parse_rule(line), data.splitlines())

    return list(rules_data)


def validate_value(value, rules):
    for rule in rules:
        for (min_allowed, max_allowed) in rule["ranges"]:
            if min_allowed <= value <= max_allowed:
                return True

    return False


def get_invalid_values(tickets, rules):
    invalid_values = []

    for ticket in tickets:
        for value in ticket:
            if not validate_value(value, rules):
                invalid_values.append(value)

    return invalid_values


def validate_ticket(ticket, invalid_values):
    for value in ticket:
        if value in invalid_values:
            return False

    return True


def determine_field_position(tickets, rules):
    max_col_count = max(map(lambda ticket: len(ticket), tickets))
    possibilities = {rule["field"]: set(range(0, max_col_count)) for rule in rules}

    for ticket in tickets:
        for col, value in enumerate(ticket):
            for rule in rules:
                if col in possibilities[rule["field"]]:
                    [range_1, range_2] = rule["ranges"]

                    if not (
                        (range_1[0] <= value <= range_1[1])
                        or (range_2[0] <= value <= range_2[1])
                    ):
                        possibilities[rule["field"]].remove(col)

    return reduce_possibilities(possibilities)


def reduce_possibilities(possibilities):
    should_reduce = True in map(lambda x: len(x) > 1, possibilities.values())

    if not should_reduce:
        return possibilities

    reserved_columns = reduce(
        lambda a, v: a.union(v), filter(lambda x: len(x) == 1, possibilities.values())
    )

    for field, possibility in possibilities.items():
        if len(possibility) >= 2:
            possibilities[field] = possibility.difference(reserved_columns)

    return reduce_possibilities(possibilities)


def find_answer_1(input):
    [rules_data, my_ticket_data, tickets_data] = input

    rules = parse_rules(rules_data)
    tickets = map(
        lambda line: [int(x) for x in line.split(",")], tickets_data.splitlines()[1:]
    )

    return reduce(lambda a, v: a + v, get_invalid_values(tickets, rules))


def find_answer_2(input):
    [rules_data, my_ticket_data, tickets_data] = input

    rules = parse_rules(rules_data)
    tickets = list(
        map(
            lambda line: [int(x) for x in line.split(",")],
            tickets_data.splitlines()[1:],
        )
    )
    my_ticket = list(
        map(
            lambda x: int(x),
            my_ticket_data.splitlines()[1].split(","),
        )
    )

    valid_tickets = list(
        filter(
            lambda ticket: validate_ticket(
                ticket, set(get_invalid_values(tickets, rules))
            ),
            tickets,
        )
    )
    field_positions = determine_field_position(valid_tickets, rules)

    return reduce(
        lambda a, v: a * my_ticket[list(field_positions[v])[0]],
        filter(lambda field: "departure" in field, list(field_positions)),
        1,
    )


if __name__ == "__main__":
    with open("day16.txt") as f:
        input = [str(x) for x in f.read().split("\n\n")]

    print(find_answer_1(input))
    print(find_answer_2(input))
