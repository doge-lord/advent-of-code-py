from functools import reduce
from operator import itemgetter
from copy import deepcopy
import re


def parse_line(line: str):
    match = re.findall(r"(ne|se|nw|sw|w|e)", line)

    if match:
        return match


def get_coordinate(origin: tuple, direction: str):
    (x, y, z) = origin
    (new_x, new_y, new_z) = origin

    if direction == "e":
        new_x += 1 if y == 0 or z == 0 else 0
        new_y -= 1 if new_x == 0 else 0
        new_z -= 1 if new_x == 0 else 0
    elif direction == "w":
        new_x -= 1 if x > 0 else 0
        new_y += 1 if x == 0 else 0
        new_z += 1 if x == 0 else 0
    elif direction == "nw":
        new_y += 1 if x == 0 or z == 0 else 0
        new_x -= 1 if new_y == 0 else 0
        new_z -= 1 if new_y == 0 else 0
    elif direction == "se":
        new_y -= 1 if y > 0 else 0
        new_x += 1 if y == 0 else 0
        new_z += 1 if y == 0 else 0
    elif direction == "sw":
        new_z += 1 if x == 0 or y == 0 else 0
        new_x -= 1 if new_z == 0 else 0
        new_y -= 1 if new_z == 0 else 0
    elif direction == "ne":
        new_z -= 1 if z > 0 else 0
        new_x += 1 if z == 0 else 0
        new_y += 1 if z == 0 else 0

    return (new_x, new_y, new_z)


def count_adjacent_black_tiles(coordinates: tuple, tile_state: dict):
    adjacent_tiles = map(
        lambda direction: get_coordinate(coordinates, direction),
        ["e", "w", "nw", "se", "sw", "ne"],
    )

    count = 0
    for adjacent_tile in adjacent_tiles:
        if tile_state.get(adjacent_tile):
            count += 1
    return count


def get_initial_tile_state(input):
    tiles = map(parse_line, input)
    tile_state = {}

    for directions in tiles:
        x = 0
        y = 0
        z = 0

        for direction in directions:
            (x, y, z) = get_coordinate((x, y, z), direction)

        if tile_state.get((x, y, z)) == None:
            tile_state[(x, y, z)] = True
        else:
            tile_state[(x, y, z)] = not tile_state[(x, y, z)]

    return tile_state


def run_cycle(tile_state: dict):
    next_tile_state = deepcopy(tile_state)

    max_x = max(map(itemgetter(0), tile_state))
    max_y = max(map(itemgetter(1), tile_state))
    max_z = max(map(itemgetter(2), tile_state))

    for x in range(0, max_x + 2):
        for y in range(0, max_y + 2):
            for z in range(0, max_z + 2):
                if x > 0 and y > 0 and z > 0:
                    continue

                count = count_adjacent_black_tiles((x, y, z), tile_state)

                if tile_state.get((x, y, z)):
                    if count == 0 or count > 2:
                        next_tile_state[(x, y, z)] = False
                else:
                    if count == 2:
                        next_tile_state[(x, y, z)] = True

    return next_tile_state


def find_answer_1(input):
    tile_state = get_initial_tile_state(input)

    return reduce(lambda a, v: a + 1 if v else a, tile_state.values(), 0)


def find_answer_2(input):
    tile_state = get_initial_tile_state(input)

    days = 100
    current_day = 1
    while current_day <= days:
        tile_state = run_cycle(tile_state)
        current_day += 1

    return reduce(lambda a, v: a + 1 if v else a, tile_state.values(), 0)


if __name__ == "__main__":
    with open("day24.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
