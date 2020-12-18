import re


def parse_input(input):
    bag_rules = {}

    for line in input:
        [subject, predicate] = (
            re.sub(r"bags?", "", line).replace(".", "").split("contain")
        )

        contents = {}

        for content in [x.strip() for x in predicate.split(",")]:
            match = re.match(r"(\d+)\s([a-z]+\s[a-z]+)", content)
            if match:
                contents[match.group(2).strip()] = int(match.group(1))
        else:
            bag_rules[subject.strip()] = contents

    return bag_rules


def find_colors_that_will_eventually_contain(color, bag_rules):
    filtered_bag_rules = dict(filter(lambda x: color in x[1], bag_rules.items()))
    colors = list(filtered_bag_rules)

    for bag_color, rules in filtered_bag_rules.items():
        colors.extend(find_colors_that_will_eventually_contain(bag_color, bag_rules))

    return set(colors)


def count_required_bags(color, bag_rules):
    count = 0

    for k, v in bag_rules[color].items():
        count += v
        count += v * count_required_bags(k, bag_rules)

    return count


def find_answer_1(input):
    bag_rules = parse_input(input)

    return len(find_colors_that_will_eventually_contain("shiny gold", bag_rules))


def find_answer_2(input):
    bag_rules = parse_input(input)

    return count_required_bags("shiny gold", bag_rules)


if __name__ == "__main__":
    with open("day07.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
