import regex


class MessageRules:
    cache = {}

    def __init__(self, input):
        rules_data = input[0].splitlines()
        rules = {}

        for rule in rules_data:
            [rule_id, rule_data] = rule.split(": ")
            rules[int(rule_id)] = rule_data

        self.rules = rules

    def get_rules(self, rule_id):
        if self.cache.get(rule_id):
            return self.cache.get(rule_id)

        rule = self.rules[rule_id].strip()

        match = regex.match(r"\"([a-b])\"", rule)
        if match:
            return [match.group(1)]

        sub_rules = []
        for sub_rules_data in rule.split("|"):
            temp_sub_rules = None

            for sub_rule_id in sub_rules_data.strip().split(" "):
                sub_rule = self.get_rules(int(sub_rule_id))

                if not temp_sub_rules:
                    temp_sub_rules = sub_rule
                    continue

                new_temp_sub_rules = []
                for x in temp_sub_rules:
                    for y in sub_rule:
                        new_temp_sub_rules.append(x + y)
                else:
                    temp_sub_rules = new_temp_sub_rules

            sub_rules.extend(temp_sub_rules)

        self.cache[rule_id] = sub_rules

        return sub_rules


def find_answer_1(input):
    message_rules = MessageRules(input)
    rule = message_rules.get_rules(0)

    count = 0
    for message in input[1].splitlines():
        for text in rule:
            if text == message:
                count += 1

    return count


def find_answer_2(input):
    message_rules = MessageRules(input)

    rule_42 = "|".join(message_rules.get_rules(42))
    rule_31 = "|".join(message_rules.get_rules(31))

    expr = regex.compile(
        "^({rule_42})+((?1)(?2)*({rule_31}))$".format(rule_42=rule_42, rule_31=rule_31)
    )

    count = 0
    for message in input[1].splitlines():
        match = regex.search(expr, message)
        if match:
            count += 1

    return count


if __name__ == "__main__":
    with open("day19.txt") as f:
        input = [str(x) for x in f.read().split("\n\n")]

    print(find_answer_1(input))
    print(find_answer_2(input))
