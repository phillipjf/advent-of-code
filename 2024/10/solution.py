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
        (-0, -1),
        (-1, 0),
        (1, 0),
        (-0, 1),
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


# Python program to search word in 2D grid in 8 directions
# This function searches for the given word
# in all 8 directions from the coordinate.
def search_2d(word: str, grid: List[str], x: int, y: int):
    y_max = len(grid)
    x_max = len(grid[0])

    if grid[y][x] != word[0]:
        return False

    len_word = len(word)

    adjacent_coordinates = get_adjacent_coordinates(x, y, x_max, y_max)
    for dir in adjacent_coordinates:
        xx = x + dir[0]
        yy = y + dir[1]
        k = 1

        while k < len_word:
            if not is_valid_coordinate(xx, yy, x_max, y_max):
                logging.debug(f"Coordinate at ({xx}, {yy}) is invalid.")
                break
            curr_val = grid[yy][xx]
            logging.debug(f"Coordinate at ({xx}, {yy}) is '{curr_val}'.")
            if curr_val != word[k]:
                break

            xx += dir[0]
            yy += dir[1]

            k += 1

        if k == len_word:
            return True

    return False


def search_word(word: str, grid: List[str]):
    y_max = len(grid)
    x_max = len(grid[0])

    ans = []
    for y in range(y_max):
        for x in range(x_max):
            # if the word is found from this coordinate, then append it to result.
            if search_2d(word, grid, x, y):
                ans.append((x, y))
    return ans


def print_result(ans):
    for coord in ans:
        print(f"{{{coord[0]},{coord[1]}}}", end=" ")
    print()


def main(part: int):
    with open("input.3.sample") as f:
        inf: List[str] = f.read().splitlines()
    word: str = "0123456789"
    result = search_word(word, inf)
    print_result(result)
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
