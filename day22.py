import re


def parse_to_game_state(input):
    game_state = {}

    for player_deck in input.split("\n\n"):
        player = None
        player_cards = []

        for i, card in enumerate(player_deck.splitlines()):
            if i == 0:
                match = re.search(r"Player\s(\d):", card)
                player = int(match.group(1))
                continue

            player_cards.append(int(card))

        game_state[player] = player_cards

    return game_state


def calculate_score(cards):
    score = 0
    for i, card in enumerate(cards):
        multiplier = len(cards) - i
        score += card * multiplier

    return score


def get_hash(p1: list, p2: list):
    return hash((",".join(map(str, p1)), ",".join(map(str, p2))))


def play_round(input_p1: list, input_p2: list, recurse: bool):
    p1 = list(input_p1)
    p2 = list(input_p2)

    p1_card = p1.pop(0)
    p2_card = p2.pop(0)

    if recurse and (len(p1) >= p1_card and len(p2) >= p2_card):
        result = play_game(p1[:p1_card], p2[:p2_card], recurse)

        if result[0] == 1:
            # P1 wins
            p1.append(p1_card)
            p1.append(p2_card)
        elif result[0] == 2:
            # P2 wins
            p2.append(p2_card)
            p2.append(p1_card)

    else:
        # They can't be equal
        if p1_card > p2_card:
            # P1 wins
            p1.append(p1_card)
            p1.append(p2_card)

        elif p1_card < p2_card:
            # P2 wins
            p2.append(p2_card)
            p2.append(p1_card)

    return (p1, p2)


def play_game(input_p1: list, input_p2: list, recurse=False):
    history = []
    winner = None  # 1 or 2

    p1 = list(input_p1)
    p2 = list(input_p2)

    round = 0
    while not (len(p1) == 0 or len(p2) == 0):
        round += 1
        round_hash = get_hash(p1, p2)

        if round_hash in history:
            # Player 1 wins
            winner = 1
            break

        (p1, p2) = play_round(p1, p2, recurse)
        history.append(round_hash)

    if not winner:
        # Player 1 wins
        if len(p1) > 0:
            winner = 1
        # Player 2 wins
        elif len(p2) > 0:
            winner = 2

    return (winner, p1, p2)


def find_answer_1(input):
    init_state = parse_to_game_state(input)

    (winner, p1, p2) = play_game(init_state[1], init_state[2])

    if winner == 1:
        return calculate_score(p1)
    else:
        return calculate_score(p2)


def find_answer_2(input):
    init_state = parse_to_game_state(input)

    (winner, p1, p2) = play_game(init_state[1], init_state[2], recurse=True)

    if winner == 1:
        return calculate_score(p1)
    else:
        return calculate_score(p2)


if __name__ == "__main__":
    with open("day22.txt") as f:
        input = f.read()

    print(find_answer_1(input))
    print(find_answer_2(input))
