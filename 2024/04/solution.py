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
        (-1, -1),
        (-0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (-0, 1),
        (1, 1),
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


def search_word(word: str, inf: List[str]) -> int:
    result = 0
    coords = []
    x_max = len(inf[0]) - 1
    y_max = len(inf) - 1
    for y, row in enumerate(inf):
        for x, col in enumerate(row):
            if inf[y][x] == word[0]:
                logging.debug(f"Found {word[0]} at ({x},{y})")
                adjacent_coordinates = get_adjacent_coordinates(x, y, x_max, y_max)
                logging.debug(f"Adjacent coordinates: {adjacent_coordinates}")
                for ac in adjacent_coordinates:
                    xx = x + ac[0]
                    yy = y + ac[1]
                    if not is_valid_coordinate(xx, yy, x_max, y_max):
                        logging.debug(f"Coordinate at ({xx}, {yy}) is invalid.")
                        continue
                    logging.debug(f"Checking for {word[1]} at ({xx}, {yy})")
                    if inf[yy][xx] == word[1]:
                        logging.debug(f"Found {word[1]} at ({xx}, {yy})")
                        xxx = xx + ac[0]
                        yyy = yy + ac[1]
                        if not is_valid_coordinate(xxx, yyy, x_max, y_max):
                            logging.debug(f"Coordinate at ({xxx}, {yyy}) is invalid.")
                            continue
                        logging.debug(f"Checking for {word[2]} at ({xxx}, {yyy})")
                        if inf[yyy][xxx] == word[2]:
                            logging.debug(f"Found {word[2]} at ({xxx}, {yyy})")
                            xxxx = xxx + ac[0]
                            yyyy = yyy + ac[1]
                            if not is_valid_coordinate(xxxx, yyyy, x_max, y_max):
                                logging.debug(
                                    f"Coordinate at ({xxxx}, {yyyy}) is invalid."
                                )
                                continue
                            logging.debug(f"Checking for {word[3]} at ({xxxx}, {yyyy})")
                            if inf[yyyy][xxxx] == word[3]:
                                logging.debug(f"Found {word[3]} at ({xxxx}, {yyyy})")
                                logging.debug(f"Found {word}!")
                                coords.extend(
                                    [(x, y), (xx, yy), (xxx, yyy), (xxxx, yyyy)]
                                )
                                result += 1
    n_col = []
    for y, row in enumerate(inf):
        n_row = ""
        for x, col in enumerate(row):
            if (x, y) in coords:
                n_row += col
            else:
                n_row += "."
        n_col.append(n_row)
    grid = "\n".join(n_col)
    logging.debug(f"\n{grid}")
    return result


def main(part: int):
    with open("input") as f:
        inf: List[str] = f.read().splitlines()
    if part == 1:
        word = "XMAS"
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
