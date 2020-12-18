from functools import reduce
import re


def parse_passport_data(data):
    parsed_data = {
        "byr": 0,
        "iyr": 0,
        "eyr": 0,
        "hgt": {"unit": None, "value": 0},
        "hcl": None,
        "ecl": None,
        "pid": None,
        "cid": None,
    }

    for x in re.split(r"\s+", data):
        year_match = re.match(r"^(byr|iyr|eyr):(\d{4})$", x)
        height_match = re.match(r"^(hgt):(\d+)(cm|in)$", x)
        hair_color_match = re.match(r"^(hcl):(#[0-9a-f]{6})$", x)
        eye_color_match = re.match(r"^(ecl):(amb|blu|brn|gry|grn|hzl|oth)$", x)
        passport_id_match = re.match(r"^(pid):(\d{9})$", x)
        country_id_match = re.match(r"^(cid):(.*)$", x)

        if year_match:
            parsed_data[year_match.group(1)] = int(year_match.group(2))

        if height_match:
            parsed_data[height_match.group(1)] = {
                "value": int(height_match.group(2)),
                "unit": height_match.group(3),
            }

        if hair_color_match:
            parsed_data[hair_color_match.group(1)] = hair_color_match.group(2)

        if eye_color_match:
            parsed_data[eye_color_match.group(1)] = eye_color_match.group(2)

        if passport_id_match:
            parsed_data[passport_id_match.group(1)] = passport_id_match.group(2)

        if country_id_match:
            parsed_data[country_id_match.group(1)] = country_id_match.group(2)

    return parsed_data


def is_valid_passport_1(data):
    fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    return reduce(lambda acc, x: acc and x in data, fields, True)


def is_valid_passport_2(data):
    validations = [
        lambda x: 1920 <= x["byr"] <= 2002,
        lambda x: 2010 <= x["iyr"] <= 2020,
        lambda x: 2020 <= x["eyr"] <= 2030,
        lambda x: (x["hgt"]["unit"] == "cm" and 150 <= x["hgt"]["value"] <= 193)
        or (x["hgt"]["unit"] == "in" and 59 <= x["hgt"]["value"] <= 76),
        lambda x: bool(x["hcl"]),
        lambda x: bool(x["ecl"]),
        lambda x: bool(x["pid"]),
    ]

    passport_data = parse_passport_data(data)

    return reduce(lambda acc, v: acc and v(passport_data), validations, True)


def find_answer_1(input):
    return len(list(filter(lambda x: is_valid_passport_1(x), input)))


def find_answer_2(input):
    return len(list(filter(lambda x: is_valid_passport_2(x), input)))


if __name__ == "__main__":
    with open("day04.txt") as f:
        input = f.read().split("\n\n")

    print(find_answer_1(input))
    print(find_answer_2(input))
