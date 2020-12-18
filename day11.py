from functools import reduce
from copy import deepcopy


class SeatLayout:
    OCCUPIED = "#"
    EMPTY = "L"
    FLOOR = "."

    prev_state = None

    def __init__(self, input):
        self.state = {}

        for y, row in enumerate(input):
            self.state[y] = {}

            for x, value in enumerate(row):
                self.state[y][x] = value

    def get_value(self, coordinates: tuple):
        (x, y) = coordinates

        if not self.state.get(y):
            return None

        return self.state[y].get(x)

    def set_value(self, coordinates: tuple, is_occupied: bool):
        (x, y) = coordinates
        if not self.get_value((x, y)) == self.FLOOR:
            self.state[y][x] = self.OCCUPIED if is_occupied else self.EMPTY

    def get_adjacent_seats(self, coordinates: tuple):
        (x, y) = coordinates
        offsets = [-1, 0, 1]
        adjacent_seats = []

        for offset_y in offsets:
            for offset_x in offsets:
                adjacent_x = x + offset_x
                adjacent_y = y + offset_y

                if adjacent_x == x and adjacent_y == y:
                    continue

                if self.get_value((adjacent_x, adjacent_y)) == self.FLOOR:
                    continue

                adjacent_seats.append((adjacent_x, adjacent_y))

        return adjacent_seats

    def get_visible_seats(self, coordinates: tuple):
        (x, y) = coordinates
        offsets = [-1, 0, 1]
        visible_seats = []

        for offset_y in offsets:
            for offset_x in offsets:
                visible_x = x + offset_x
                visible_y = y + offset_y

                if visible_x == x and visible_y == y:
                    continue

                while self.get_value((visible_x, visible_y)) == self.FLOOR:
                    visible_x += offset_x
                    visible_y += offset_y

                if self.get_value((visible_x, visible_y)):
                    visible_seats.append((visible_x, visible_y))

        return visible_seats

    def get_occupied_seats_count(self):
        count = 0
        for row in self.state.values():
            for cell in row.values():
                if cell == self.OCCUPIED:
                    count += 1
        return count

    def did_state_change(self):
        return not self.state == self.prev_state

    def display_state(self):
        for row in self.state.values():
            text = "".join(row.values())
            print(text)
        print()

    def run_round(self):
        set_to_occupied = []
        set_to_empty = []

        for y, row in self.state.items():
            for x, cell in row.items():
                if cell == SeatLayout.FLOOR:
                    continue

                adjacent_occupied_seats = reduce(
                    lambda a, v: a + 1 if self.get_value(v) == self.OCCUPIED else a,
                    self.get_adjacent_seats((x, y)),
                    0,
                )

                if cell == self.EMPTY and adjacent_occupied_seats == 0:
                    set_to_occupied.append((x, y))
                elif cell == self.OCCUPIED and adjacent_occupied_seats >= 4:
                    set_to_empty.append((x, y))

        # Snapshot previous state
        self.prev_state = deepcopy(self.state)

        # Apply changes
        for coordinates in set_to_occupied:
            self.set_value(coordinates, True)

        for coordinates in set_to_empty:
            self.set_value(coordinates, False)

    def run_round_v2(self):
        set_to_occupied = []
        set_to_empty = []

        for y, row in self.state.items():
            for x, cell in row.items():
                if cell == SeatLayout.FLOOR:
                    continue

                visible_occupied_seats = reduce(
                    lambda a, v: a + 1 if self.get_value(v) == self.OCCUPIED else a,
                    self.get_visible_seats((x, y)),
                    0,
                )

                if cell == self.EMPTY and visible_occupied_seats == 0:
                    set_to_occupied.append((x, y))
                elif cell == self.OCCUPIED and visible_occupied_seats >= 5:
                    set_to_empty.append((x, y))

        # Snapshot previous state
        self.prev_state = deepcopy(self.state)

        # Apply changes
        for coordinates in set_to_occupied:
            self.set_value(coordinates, True)

        for coordinates in set_to_empty:
            self.set_value(coordinates, False)


def find_answer_1(input):
    seat_layout = SeatLayout(input)

    while seat_layout.did_state_change():
        seat_layout.run_round()

    return seat_layout.get_occupied_seats_count()


def find_answer_2(input):
    seat_layout = SeatLayout(input)

    while seat_layout.did_state_change():
        seat_layout.run_round_v2()

    return seat_layout.get_occupied_seats_count()


if __name__ == "__main__":
    with open("day11.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
