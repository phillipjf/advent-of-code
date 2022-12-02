"""
|          |   |   |   |
| rock     | A | X | 1 |
| paper    | B | Y | 2 |
| scissors | C | Z | 3 |
| lose     |   | X | 0 |
| draw     |   | Y | 3 |
| win      |   | Z | 6 |


total score = sum of my score each round
score round = shape point + outcome
"""
from typing import Dict, List

lookup: Dict[str, str] = {
    "A": "X",
    "B": "Y",
    "C": "Z",
    "X": "lose",
    "Y": "draw",
    "Z": "win",
}
scores: Dict[str, int] = {"X": 1, "Y": 2, "Z": 3, "win": 6, "lose": 0, "draw": 3}
scoring: Dict[str, Dict[str, str]] = {
    "A": {"win": "Y", "lose": "Z", "draw": "X", "Y": "win", "Z": "lose", "X": "draw"},
    "B": {"win": "Z", "lose": "X", "draw": "Y", "Z": "win", "X": "lose", "Y": "draw"},
    "C": {"win": "X", "lose": "Y", "draw": "Z", "X": "win", "Y": "lose", "Z": "draw"},
}


def score_round(opponent: str, me: str) -> int:
    score: int = 0
    my_score: int = scores[me]
    score += my_score

    score += scores[scoring[opponent][me]]

    # if lookup[opponent] == me:
    #     score += 3
    #     return score

    # if opponent == "A":
    #     if me == "Y":
    #         score += 6
    #     if me == "Z":
    #         score += 0
    # elif opponent == "B":
    #     if me == "X":
    #         score += 0
    #     if me == "Z":
    #         score += 6
    # elif opponent == "C":
    #     if me == "X":
    #         score += 6
    #     if me == "Y":
    #         score += 0
    return score


def choose_move(opponent: str, outcome: str) -> int:
    _outcome: str = lookup[outcome]
    _me: str = scoring[opponent][_outcome]
    outcome_score: int = scores[_outcome]
    my_score: int = scores[_me]
    total_score: int = outcome_score + my_score

    # print(
    #     f"{_outcome} ({outcome}, {outcome_score}) | {opponent} v. {_me}({my_score}) | {total_score}"
    # )
    return total_score


if __name__ == "__main__":
    with open("input") as f:
        inf = f.read()

    rounds: List[str] = inf.split("\n")

    total_score_1: int = 0
    total_score_2: int = 0
    for round in rounds:
        opponent: str
        me: str
        opponent, me = round.split(" ")
        total_score_1 += score_round(opponent, me)
        total_score_2 += choose_move(opponent, me)
        print(f"{total_score_1}, {total_score_2}")
