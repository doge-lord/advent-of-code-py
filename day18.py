import re


def find_closing_parenthesis_index(expression: str):
    group_open_count = 0
    group_close_count = 0

    for i, char in enumerate(list(expression)):
        if char == "(":
            group_open_count += 1
        elif char == ")":
            group_close_count += 1

        if group_open_count == group_close_count:
            return i


def strip_outer_parentheses(expression: str):
    if find_closing_parenthesis_index(expression) == len(expression) - 1:
        pr_match = re.match(r"^\((.*)\)$", expression.strip())
        if pr_match:
            return strip_outer_parentheses(pr_match.group(1).strip())

    return expression.strip()


def reduce_expression(input: str):
    expression = strip_outer_parentheses(input)
    current = None
    current_op = "+"
    accumulator = 0

    while len(expression.strip()) > 0:
        expression = expression.strip()

        if expression[0] in ["*", "+"]:
            current_op = expression[0]
            expression = expression.replace(expression[0], "", 1).strip()
            continue

        current = None

        if expression[0] == "(":
            current = expression[0 : find_closing_parenthesis_index(expression) + 1]

            if current_op == "+":
                accumulator += reduce_expression(current)
            elif current_op == "*":
                accumulator *= reduce_expression(current)

            expression = expression.replace(current, "", 1).strip()

        else:
            match = re.match(r"^(\d+)", expression)
            current = match.group(1)

            if current_op == "+":
                accumulator += int(current)
            elif current_op == "*":
                accumulator *= int(current)

        expression = expression.replace(current, "", 1).strip()

    return accumulator


def reduce_expression_v2(input: str):
    expression = input.strip()

    # Groupings
    group_expr = re.findall(r"\([\d\s\+\*]+\)", expression)
    if len(group_expr):
        for expr in group_expr:
            expression = expression.replace(
                expr, reduce_expression_v2(expr.strip("()")), 1
            ).strip()

        return reduce_expression_v2(expression)

    # Addition
    addition_expr = re.findall(r"\d+\s\+\s\d+", expression)
    if len(addition_expr):
        for expr in addition_expr:
            (add_1, add_2) = expr.split(" + ")
            sum = int(add_1) + int(add_2)

            expression = expression.replace(expr, str(sum), 1).strip()

        return reduce_expression_v2(expression)

    # Multiplication
    multiplication_expr = re.findall(r"\d+\s\*\s\d+", expression)
    if len(multiplication_expr):
        for expr in multiplication_expr:
            (mult_1, mult_2) = expr.split(" * ")
            product = int(mult_1) * int(mult_2)

            expression = expression.replace(expr, str(product), 1).strip()

        return reduce_expression_v2(expression)

    return expression


def find_answer_1(input):
    sum = 0
    for expression in input:
        sum += int(reduce_expression(expression))

    return sum


def find_answer_2(input):
    sum = 0
    for expression in input:
        sum += int(reduce_expression_v2(expression))

    return sum


if __name__ == "__main__":
    with open("day18.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
