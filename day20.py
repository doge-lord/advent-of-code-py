import re
from operator import itemgetter
from copy import deepcopy


def display_tile(tile):
    for row in tile:
        print("".join(row))
    else:
        print()


def rotate_tile(tile):
    # Rotate clockwise
    new_tile = []

    for row_number, row in enumerate(reversed(tile)):
        for col_number, cell in enumerate(row):
            if row_number == 0:
                new_tile.append([])

            new_tile[col_number].append(cell)

    return new_tile


def flip_tile_x(tile):
    new_tile = []

    for row in tile:
        new_tile.append(list(reversed(row)))

    return new_tile


def flip_tile_y(tile):
    return list(reversed(tile))


def transform_tile(tile, flip_x, flip_y, rotation):
    new_tile = tile

    for _ in range(0, rotation):
        new_tile = rotate_tile(new_tile)

    if flip_x:
        new_tile = flip_tile_x(new_tile)

    if flip_y:
        new_tile = flip_tile_y(new_tile)

    return new_tile


def get_border_left(tile):
    border = ""

    for row in tile:
        border += row[0]

    return border


def get_border_right(tile):
    border = ""

    for row in tile:
        border += row[-1]

    return border


def get_border_top(tile):
    return "".join(tile[0])


def get_border_bottom(tile):
    return "".join(tile[-1])


def get_flip_rotation_combinations():
    flip_values = [True, False]
    # We only need to rotate once since rotating the tile twice or thrice
    # can be reproduced by flipping both axis
    rotation_values = list(range(0, 2))

    flip_rotate_combinations = []

    for flip_x in flip_values:
        for flip_y in flip_values:
            for rotation in rotation_values:
                flip_rotate_combinations.append((flip_x, flip_y, rotation))

    return flip_rotate_combinations


def get_sea_monster_pattern():
    sea_monster_raw_pattern = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]

    sea_monster_coordinates = []

    for y, row in enumerate(sea_monster_raw_pattern):
        for x, cell in enumerate(row):
            if cell == "#":
                sea_monster_coordinates.append((x, y))

    return sea_monster_coordinates


def find_sea_monsters(tile):
    sea_monster_coordinates = get_sea_monster_pattern()

    new_tile_data = deepcopy(tile)

    for y, row in enumerate(tile):
        for x, cell in enumerate(row):
            is_sea_monster = True

            try:
                for off_x, off_y in sea_monster_coordinates:
                    if not new_tile_data[y + off_y][x + off_x] == "#":
                        is_sea_monster = False
                        break
            except:
                is_sea_monster = False

            if is_sea_monster:
                for off_x, off_y in sea_monster_coordinates:
                    new_tile_data[y + off_y][x + off_x] = "O"

    return new_tile_data


def has_sea_monster(tile):
    for row in tile:
        for cell in row:
            if cell == "O":
                return True

    return False


def determine_water_roughness(tile):
    count = 0

    for row in tile:
        for cell in row:
            if cell == "#":
                count += 1

    return count


class CameraArray:
    assembled_image = None

    def __init__(self, input):
        self.tiles = {}

        for tile_data in input:
            tile_id = None
            rows = []

            for i, line in enumerate(tile_data.splitlines()):
                if i == 0:
                    match = re.match(r"Tile (\d+):", line)
                    if match:
                        tile_id = int(match.group(1))
                        continue

                rows.append(list(line))

            self.tiles[tile_id] = rows

    def get_tile(self, tile_id: int):
        return self.tiles.get(tile_id)

    def get_connections(self):
        possible_connections = {}
        tiles = set(self.tiles)

        for tile_id_1 in tiles:
            connections = []

            for tile_id_2 in tiles.difference([tile_id_1]):
                tile_1 = self.get_tile(tile_id_1)
                tile_2 = self.get_tile(tile_id_2)

                tile_1_top = get_border_top(tile_1)
                tile_1_left = get_border_left(tile_1)
                tile_1_bottom = get_border_bottom(tile_1)
                tile_1_right = get_border_right(tile_1)

                cxn = []

                for flip_x, flip_y, rotation in get_flip_rotation_combinations():
                    transformed_tile_2 = transform_tile(
                        tile_2,
                        flip_x,
                        flip_y,
                        rotation,
                    )

                    tile_2_top = get_border_top(transformed_tile_2)
                    tile_2_left = get_border_left(transformed_tile_2)
                    tile_2_bottom = get_border_bottom(transformed_tile_2)
                    tile_2_right = get_border_right(transformed_tile_2)

                    # Top
                    if tile_1_top == tile_2_bottom:
                        cxn.append((tile_id_2, "top"))

                    # Left
                    if tile_1_left == tile_2_right:
                        cxn.append((tile_id_2, "left"))

                    # Bottom
                    if tile_1_bottom == tile_2_top:
                        cxn.append((tile_id_2, "bottom"))

                    # Right
                    if tile_1_right == tile_2_left:
                        cxn.append((tile_id_2, "right"))

                connections.extend(cxn)

            possible_connections[tile_id_1] = connections

        return possible_connections

    def assemble_tiles(self):
        possible_connections = self.get_connections()

        unused_tiles = list(self.tiles)
        (starting_tile, _) = sorted(
            possible_connections.items(), key=lambda x: len(x[1])
        )[0]

        assembled_image = {starting_tile: ((0, 0), self.get_tile(starting_tile))}
        unused_tiles.remove(starting_tile)
        tiles_read = set()

        while len(unused_tiles) > 0:
            tile_to_read = set(list(assembled_image)).difference(tiles_read).pop()
            (position, tile_data) = assembled_image[tile_to_read]
            (x, y) = position

            tile_1_top = get_border_top(tile_data)
            tile_1_left = get_border_left(tile_data)
            tile_1_bottom = get_border_bottom(tile_data)
            tile_1_right = get_border_right(tile_data)

            for ctile_id, _ in possible_connections[tile_to_read]:
                if ctile_id in list(assembled_image):
                    continue

                for flip_x, flip_y, rotation in get_flip_rotation_combinations():
                    transformed_tile_2 = transform_tile(
                        self.get_tile(ctile_id),
                        flip_x,
                        flip_y,
                        rotation,
                    )

                    tile_2_top = get_border_top(transformed_tile_2)
                    tile_2_left = get_border_left(transformed_tile_2)
                    tile_2_bottom = get_border_bottom(transformed_tile_2)
                    tile_2_right = get_border_right(transformed_tile_2)

                    # Top
                    if tile_1_top == tile_2_bottom:
                        assembled_image[ctile_id] = ((x, y - 1), transformed_tile_2)
                        unused_tiles.remove(ctile_id)
                        break

                    # Left
                    if tile_1_left == tile_2_right:
                        assembled_image[ctile_id] = ((x - 1, y), transformed_tile_2)
                        unused_tiles.remove(ctile_id)
                        break

                    # Bottom
                    if tile_1_bottom == tile_2_top:
                        assembled_image[ctile_id] = ((x, y + 1), transformed_tile_2)
                        unused_tiles.remove(ctile_id)
                        break

                    # Right
                    if tile_1_right == tile_2_left:
                        assembled_image[ctile_id] = ((x + 1, y), transformed_tile_2)
                        unused_tiles.remove(ctile_id)
                        break

            tiles_read.add(tile_to_read)

        coordinate_tile_data = sorted(assembled_image.values(), key=itemgetter(0))
        tile_length = len(coordinate_tile_data[0][1][0])
        lines = {}

        for pos, tile_data in coordinate_tile_data:
            (x, y) = pos

            for row_num, row in enumerate(tile_data):
                if row_num in [0, 9]:
                    continue

                line_row_id = y * tile_length + row_num

                if not lines.get(line_row_id):
                    lines[line_row_id] = "".join(row[1:9])
                else:
                    lines[line_row_id] += "".join(row[1:9])

        assembled_image = []
        for line in lines.values():
            assembled_image.append(list(line))

        self.assembled_image = assembled_image


def find_answer_1(input):
    camera_array = CameraArray(input)

    tile_ids_product = 1

    for tile_id, connections in camera_array.get_connections().items():
        if len(connections) == 2:
            tile_ids_product *= tile_id

    return tile_ids_product


def find_answer_2(input):
    camera_array = CameraArray(input)
    camera_array.assemble_tiles()

    for flip_x, flip_y, rotation in get_flip_rotation_combinations():
        image = find_sea_monsters(
            transform_tile(
                camera_array.assembled_image,
                flip_x,
                flip_y,
                rotation,
            )
        )

        if has_sea_monster(image):
            return determine_water_roughness(image)


if __name__ == "__main__":
    with open("day20.txt") as f:
        input = [str(x) for x in f.read().split("\n\n")]

    print(find_answer_1(input))
    print(find_answer_2(input))
