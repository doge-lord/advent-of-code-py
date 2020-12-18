class PocketDimension3D:
    ACTIVE = "#"
    INACTIVE = "."

    def __init__(self, input):
        self.state = {0: {}}
        self.min_z = 0
        self.max_z = 0
        self.min_y = 0
        self.max_y = len(input) - 1
        self.min_x = 0
        self.max_x = len(input[0]) - 1

        for y, row in enumerate(input):
            self.state[0][y] = {}

            for x, value in enumerate(row):
                self.state[0][y][x] = value

    def display_char(self, coordinates: tuple):
        value = self.get_value(coordinates)
        return value if value else self.INACTIVE

    def display_state(self):
        for z in range(self.min_z, self.max_z + 1):
            print("z =", z)
            for y in range(self.min_y, self.max_y + 1):
                text = "".join(
                    list(
                        map(
                            lambda x: self.display_char((x, y, z)),
                            range(self.min_x, self.max_x + 1),
                        )
                    )
                )
                print(text)
            print()

    def get_value(self, coordinates: tuple):
        (x, y, z) = coordinates

        if not self.state.get(z):
            return None

        if not self.state[z].get(y):
            return None

        return self.state[z][y].get(x)

    def set_value(self, coordinates: tuple, is_active: bool):
        (x, y, z) = coordinates

        if z < self.min_z:
            self.min_z = z
        elif z > self.max_z:
            self.max_z = z

        if y < self.min_y:
            self.min_y = y
        elif y > self.max_y:
            self.max_y = y

        if x < self.min_x:
            self.min_x = x
        elif x > self.max_x:
            self.max_x = x

        if not self.state.get(z):
            self.state[z] = {}

        if not self.state[z].get(y):
            self.state[z][y] = {}

        self.state[z][y][x] = self.ACTIVE if is_active else self.INACTIVE

    def get_neighbors(self, coordinates: tuple):
        (x, y, z) = coordinates
        offsets = [-1, 0, 1]
        neighbors = []

        for offset_z in offsets:
            for offset_y in offsets:
                for offset_x in offsets:
                    neighbor_x = x + offset_x
                    neighbor_y = y + offset_y
                    neighbor_z = z + offset_z

                    if neighbor_x == x and neighbor_y == y and neighbor_z == z:
                        continue

                    neighbors.append((neighbor_x, neighbor_y, neighbor_z))

        return neighbors

    def count_active_neighbors(self, coordinates: tuple):
        return len(
            list(
                filter(
                    lambda val: val == self.ACTIVE,
                    map(
                        lambda neighbor: self.get_value(neighbor),
                        self.get_neighbors(coordinates),
                    ),
                )
            )
        )

    def count_active_cubes(self):
        count = 0
        for z in range(self.min_z, self.max_z + 1):
            for y in range(self.min_y, self.max_y + 1):
                for x in range(self.min_x, self.max_x + 1):
                    if self.display_char((x, y, z)) == self.ACTIVE:
                        count += 1

        return count

    def run_cycle(self):
        set_to_active = []
        set_to_inactive = []

        for z in range(self.min_z - 1, self.max_z + 2):
            for y in range(self.min_y - 1, self.max_y + 2):
                for x in range(self.min_x - 1, self.max_x + 2):
                    active_neighbors_count = self.count_active_neighbors((x, y, z))

                    if self.get_value((x, y, z)) == self.ACTIVE:
                        if 2 <= active_neighbors_count <= 3:
                            set_to_active.append((x, y, z))
                        else:
                            set_to_inactive.append((x, y, z))
                    else:
                        if active_neighbors_count == 3:
                            set_to_active.append((x, y, z))

        # Apply changes
        for coordinates in set_to_active:
            self.set_value(coordinates, True)

        for coordinates in set_to_inactive:
            self.set_value(coordinates, False)


class PocketDimension4D:
    ACTIVE = "#"
    INACTIVE = "."

    def __init__(self, input):
        self.state = {0: {0: {}}}
        self.min_w = 0
        self.max_w = 0
        self.min_z = 0
        self.max_z = 0
        self.min_y = 0
        self.max_y = len(input) - 1
        self.min_x = 0
        self.max_x = len(input[0]) - 1

        for y, row in enumerate(input):
            self.state[0][0][y] = {}

            for x, value in enumerate(row):
                self.state[0][0][y][x] = value

    def display_char(self, coordinates: tuple):
        value = self.get_value(coordinates)
        return value if value else self.INACTIVE

    def display_state(self):
        for w in range(self.min_w, self.max_w + 1):
            for z in range(self.min_z, self.max_z + 1):
                print("z =", z, ",", "w =", w)
                for y in range(self.min_y, self.max_y + 1):
                    text = "".join(
                        list(
                            map(
                                lambda x: self.display_char((x, y, z, w)),
                                range(self.min_x, self.max_x + 1),
                            )
                        )
                    )
                    print(text)
                print()

    def get_value(self, coordinates: tuple):
        (x, y, z, w) = coordinates

        if not self.state.get(w):
            return None

        if not self.state[w].get(z):
            return None

        if not self.state[w][z].get(y):
            return None

        return self.state[w][z][y].get(x)

    def set_value(self, coordinates: tuple, is_active: bool):
        (x, y, z, w) = coordinates

        if w < self.min_w:
            self.min_w = w
        elif w > self.max_w:
            self.max_w = w

        if z < self.min_z:
            self.min_z = z
        elif z > self.max_z:
            self.max_z = z

        if y < self.min_y:
            self.min_y = y
        elif y > self.max_y:
            self.max_y = y

        if x < self.min_x:
            self.min_x = x
        elif x > self.max_x:
            self.max_x = x

        if not self.state.get(w):
            self.state[w] = {}

        if not self.state[w].get(z):
            self.state[w][z] = {}

        if not self.state[w][z].get(y):
            self.state[w][z][y] = {}

        self.state[w][z][y][x] = self.ACTIVE if is_active else self.INACTIVE

    def get_neighbors(self, coordinates: tuple):
        (x, y, z, w) = coordinates
        offsets = [-1, 0, 1]
        neighbors = []

        for offset_w in offsets:
            for offset_z in offsets:
                for offset_y in offsets:
                    for offset_x in offsets:
                        neighbor_x = x + offset_x
                        neighbor_y = y + offset_y
                        neighbor_z = z + offset_z
                        neighbor_w = w + offset_w

                        if (
                            neighbor_x == x
                            and neighbor_y == y
                            and neighbor_z == z
                            and neighbor_w == w
                        ):
                            continue

                        neighbors.append(
                            (neighbor_x, neighbor_y, neighbor_z, neighbor_w)
                        )

        return neighbors

    def count_active_neighbors(self, coordinates: tuple):
        return len(
            list(
                filter(
                    lambda val: val == self.ACTIVE,
                    map(
                        lambda neighbor: self.get_value(neighbor),
                        self.get_neighbors(coordinates),
                    ),
                )
            )
        )

    def count_active_cubes(self):
        count = 0
        for w in range(self.min_w, self.max_w + 1):
            for z in range(self.min_z, self.max_z + 1):
                for y in range(self.min_y, self.max_y + 1):
                    for x in range(self.min_x, self.max_x + 1):
                        if self.display_char((x, y, z, w)) == self.ACTIVE:
                            count += 1

        return count

    def run_cycle(self):
        set_to_active = []
        set_to_inactive = []

        for w in range(self.min_w - 1, self.max_w + 2):
            for z in range(self.min_z - 1, self.max_z + 2):
                for y in range(self.min_y - 1, self.max_y + 2):
                    for x in range(self.min_x - 1, self.max_x + 2):
                        active_neighbors_count = self.count_active_neighbors(
                            (x, y, z, w)
                        )

                        if self.get_value((x, y, z, w)) == self.ACTIVE:
                            if 2 <= active_neighbors_count <= 3:
                                set_to_active.append((x, y, z, w))
                            else:
                                set_to_inactive.append((x, y, z, w))
                        else:
                            if active_neighbors_count == 3:
                                set_to_active.append((x, y, z, w))

        # Apply changes
        for coordinates in set_to_active:
            self.set_value(coordinates, True)

        for coordinates in set_to_inactive:
            self.set_value(coordinates, False)


def find_answer_1(input):
    pocket_dimension = PocketDimension3D(input)
    count = 1

    while count <= 6:
        pocket_dimension.run_cycle()
        count += 1

    return pocket_dimension.count_active_cubes()


def find_answer_2(input):
    pocket_dimension = PocketDimension4D(input)
    count = 1

    while count <= 6:
        pocket_dimension.run_cycle()
        count += 1

    return pocket_dimension.count_active_cubes()


if __name__ == "__main__":
    with open("day17.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
