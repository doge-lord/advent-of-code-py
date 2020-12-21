from functools import reduce
from operator import itemgetter


def parse_input(input):
    ingredient_list = []

    for line in input:
        [ingredients_data, allergens_data] = line.split(" (contains ")

        ingredients = set(ingredients_data.strip().split(" "))
        allergens = set(allergens_data.strip("()").split(", "))

        ingredient_list.append((ingredients, allergens))

    return ingredient_list


def has_multiple_possibilities(possibilities):
    for possible_ingredients in possibilities.values():
        if len(possible_ingredients) > 1:
            return True

    return False


def reduce_possibilities(possibilities):
    defined_ingredients = list(
        map(
            lambda x: list(x)[0],
            filter(lambda x: len(x) == 1, possibilities.values()),
        )
    )

    new_possibilities = {}

    for allergen, ingredients in possibilities.items():
        if len(ingredients) == 1:
            new_possibilities[allergen] = ingredients
        else:
            new_possibilities[allergen] = ingredients.difference(defined_ingredients)

    return new_possibilities


def get_translations(ingredient_list):
    possibilities = {}

    for ingredients, allergens in ingredient_list:
        for allergen in allergens:
            if not possibilities.get(allergen):
                possibilities[allergen] = ingredients

            possibilities[allergen] = possibilities[allergen].intersection(ingredients)

    count = 0
    limit = 100
    while has_multiple_possibilities(possibilities):
        if count >= 100:
            print("Fail Fish")
            break

        possibilities = reduce_possibilities(possibilities)
        count += 1

    translations = {}
    for allergen, ingredients in possibilities.items():
        if len(ingredients) == 1:
            translations[allergen] = list(ingredients)[0]

    return translations


def find_answer_1(input):
    ingredient_list = parse_input(input)
    translations = get_translations(ingredient_list)
    known_allergens = translations.values()

    count = 0
    for ingredients, allergens in ingredient_list:
        count += len(ingredients.difference(known_allergens))

    return count


def find_answer_2(input):
    ingredient_list = parse_input(input)
    translations = get_translations(ingredient_list)
    known_allergens = list(
        map(itemgetter(1), sorted(translations.items(), key=itemgetter(0)))
    )

    return ",".join(known_allergens)


if __name__ == "__main__":
    with open("day21.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
