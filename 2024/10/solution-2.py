import argparse
import logging
from typing import List, Tuple
from dataclasses import dataclass, field

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


def get_adjacent_coordinates(
    x: int, y: int, x_max: int, y_max: int
) -> List[Tuple[int, int]]:
    possible_coordinates = [
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0),
    ]
    adjacent_coordinates = [
        pc
        for pc in possible_coordinates
        if (x + pc[0] >= 0 and x + pc[0] <= x_max)
        and (y + pc[1] >= 0 and y + pc[1] <= y_max)
    ]
    return adjacent_coordinates


def is_valid_coordinate(x: int, y: int, x_max: int, y_max: int) -> bool:
    return (x >= 0 and x <= x_max) and (y >= 0 and y <= y_max)


def find_match(inf, word, x, y, l_idx):
    word_len = len(word)
    y_max = len(inf) - 1
    x_max = len(inf[0]) - 1

    if l_idx == word_len:
        logging.debug("Reached end of word.")
        return True

    if not is_valid_coordinate(x, y, x_max, y_max):
        logging.debug(f"Coordinate at ({x}, {y}) is invalid.")
        return False

    if inf[y][x] == word[l_idx]:
        logging.debug(f"Found {word[l_idx]} at ({x}, {y})")
        temp = inf[y][x]
        inf[y][x] = "#"
        ac = get_adjacent_coordinates(x, y, x_max, y_max)
        res = any([find_match(inf, word, x + xx, y + yy, l_idx + 1) for xx, yy in ac])
        inf[y][x] = temp
        return res

    return False


def search_word(word: str, inf: List[List[str]]):
    y_max = len(inf) - 1
    x_max = len(inf[0]) - 1

    for y in range(y_max):
        for x in range(x_max):
            if find_match(inf, word, x, y, 0):
                return True
    return False


def main(part: int):
    with open("input.3.sample") as f:
        inf: List[List[str]] = [list(l) for l in f.read().splitlines()]
    word: str = "0123456789"
    result = search_word(word, inf)
    logging.info(f"Part {'One' if part ==1 else 'Two'} Answer: {result}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "part",
        metavar="P",
        type=int,
        choices=[1, 2],
        help="Problem part (1 or 2)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Be verbose",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    args = parser.parse_args()
    if args.loglevel:
        logging.getLogger().setLevel(args.loglevel)
    main(args.part)
