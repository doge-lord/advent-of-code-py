import re
import math


def parse_line(line):
    match = re.match(r"(N|S|E|W|L|R|F)(\d+)", line)
    return (match.group(1), int(match.group(2)))


def add_angle(angle_1, angle_2):
    angle = angle_1 + angle_2

    if angle >= 360:
        return angle - 360
    if angle < 0:
        return angle + 360
    return angle


def get_xy_by_angle(angle, value):
    x = 0
    y = 0

    if angle == 0:
        x += value
    elif angle == 180:
        x -= value
    elif angle == 90:
        y += value
    elif angle == 270:
        y -= value
    else:
        angle_in_radians = math.radians(angle)
        x += value * math.tan(angle_in_radians)
        y += value / math.tan(angle_in_radians)

    return (x, y)


def get_waypoint_by_angle(x, y, angle):
    new_angle = add_angle(angle, 0)

    if new_angle == 0:
        return (x, y)
    elif new_angle == 90:
        return (-y, x)
    elif new_angle == 180:
        return (-x, -y)
    elif new_angle == 270:
        return (y, -x)


def find_answer_1(input):
    x = 0
    y = 0
    angle = 0  # in degrees

    for instruction, value in [parse_line(x) for x in input]:
        if instruction == "N":
            y += value
        if instruction == "S":
            y -= value
        if instruction == "E":
            x += value
        if instruction == "W":
            x -= value
        if instruction == "L":
            angle = add_angle(angle, value)
        if instruction == "R":
            angle = add_angle(angle, -value)
        if instruction == "F":
            (offset_x, offset_y) = get_xy_by_angle(angle, value)
            x += offset_x
            y += offset_y

    return abs(int(x)) + abs(int(y))


def find_answer_2(input):
    waypoint_x = 10
    waypoint_y = 1
    x = 0
    y = 0

    for instruction, value in [parse_line(x) for x in input]:
        if instruction == "N":
            waypoint_y += value
        if instruction == "S":
            waypoint_y -= value
        if instruction == "E":
            waypoint_x += value
        if instruction == "W":
            waypoint_x -= value
        if instruction == "L":
            (new_waypoint_x, new_waypoint_y) = get_waypoint_by_angle(
                waypoint_x, waypoint_y, value
            )
            waypoint_x = new_waypoint_x
            waypoint_y = new_waypoint_y
        if instruction == "R":
            (new_waypoint_x, new_waypoint_y) = get_waypoint_by_angle(
                waypoint_x, waypoint_y, -value
            )
            waypoint_x = new_waypoint_x
            waypoint_y = new_waypoint_y
        if instruction == "F":
            x += waypoint_x * value
            y += waypoint_y * value

    return abs(int(x)) + abs(int(y))


if __name__ == "__main__":
    with open("day12.txt") as f:
        input = [str(x) for x in f.read().splitlines()]

    print(find_answer_1(input))
    print(find_answer_2(input))
