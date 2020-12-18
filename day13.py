def get_departure_time_after(bus_id, time):
    departure_time = 0
    while departure_time < time:
        departure_time += bus_id

    return departure_time


def is_timestamp_at_matching_pos(timestamp, bus_id_offset):
    for (bus_id, offset) in bus_id_offset:
        if not (timestamp + offset) % bus_id == 0:
            return True

    return False


def find_answer_1(input):
    [can_depart_str, bus_ids_str] = input

    can_depart = int(can_depart_str)
    bus_ids = map(
        lambda bus_id: int(bus_id),
        filter(lambda bus_id: not bus_id == "x", bus_ids_str.split(",")),
    )

    bus_id_with_departure_time = list(
        map(
            lambda bus_id: (bus_id, get_departure_time_after(bus_id, can_depart)),
            bus_ids,
        )
    )
    earliest_departure_time = min(map(lambda x: x[1], bus_id_with_departure_time))

    for (bus_id, depature_time) in bus_id_with_departure_time:
        if depature_time == earliest_departure_time:
            return bus_id * (depature_time - can_depart)


def find_answer_2(input):
    [_, bus_ids_str] = input

    offset = 0
    bus_id_offset = []
    bus_ids = bus_ids_str.split(",")
    max_bus_id = max(map(lambda y: int(y), filter(lambda x: not x == "x", bus_ids)))
    max_bus_id_index = bus_ids.index(str(max_bus_id))

    for i, bus_id in enumerate(bus_ids):
        if not bus_id == "x":
            bus_id_offset.append((int(bus_id), i - max_bus_id_index))

    increment = max_bus_id
    for (bus_id, offset) in bus_id_offset:
        if bus_id == offset or bus_id == abs(offset):
            increment *= bus_id

    timestamp = increment

    while is_timestamp_at_matching_pos(timestamp, bus_id_offset):
        timestamp += increment

    return timestamp - max_bus_id_index


if __name__ == "__main__":
    with open("day13.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
