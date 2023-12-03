import argparse
import logging
import operator
import functools


from typing import List
from dataclasses import dataclass, field


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


@dataclass
class Draw:
    r: int = 0
    g: int = 0
    b: int = 0

    def valid(self):
        return all([self.r <= 12, self.g <= 13, self.b <= 14])


@dataclass
class Game:
    id_num: int
    draws: list[Draw] = field(default_factory=list)

    def valid(self):
        return all([d.valid() for d in self.draws])

    def min(self) -> List[int]:
        r = max([d.r for d in self.draws])
        g = max([d.g for d in self.draws])
        b = max([d.b for d in self.draws])
        logging.debug([r, g, b])
        return [r, g, b]

    def power(self) -> int:
        return functools.reduce(operator.mul, self.min(), 1)


def parse(s: str) -> Game:
    game, draws = s.split(": ")
    game = int(game.split(" ")[1])
    game = Game(id_num=game)
    draws = draws.split("; ")
    for draw in draws:
        d = Draw()
        cubes = draw.split(", ")
        for cube in cubes:
            c = cube.split(" ")
            if "red" in c[1]:
                d.r = int(c[0])
            if "green" in c[1]:
                d.g = int(c[0])
            if "blue" in c[1]:
                d.b = int(c[0])
        game.draws.append(d)
    return game


def main(part):
    with open("input") as f:
        inf: List[str] = f.readlines()

    possible = 0
    power = 0

    for g in inf:
        game = parse(g)
        logging.debug(f"{game}, {game.min()}, {game.power()}, {game.valid()}")
        if game.valid():
            possible += game.id_num
        power += game.power()

    logging.info(f"Part One Answer: {possible}")
    logging.info(f"Part Two Answer: {power}")


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
