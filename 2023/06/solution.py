import argparse
import logging
import operator
import functools
from typing import List
from dataclasses import dataclass


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


@dataclass
class Race:
    time: int
    dist: int

    def trials(self) -> int:
        wins = []
        for i in range(self.time + 1):
            dist = self.run(i)
            win = dist > self.dist
            logging.debug(f"Hold Time: {i}, Distance: {dist}, Win: {win}")
            if win:
                wins.append(i)
        return len(wins)

    def run(self, hold_time) -> int:
        speed = hold_time
        run_time = self.time - hold_time
        return speed * run_time


def load_data(part) -> List[Race]:
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    times: List[int] = [int(t) for t in inf[0].split(":")[1].split(" ") if t != ""]
    dists: List[int] = [int(d) for d in inf[1].split(":")[1].split(" ") if d != ""]
    races = [Race(times[i], dists[i]) for i in range(len(times))]
    logging.debug(f"Times: {times}, Dists: {dists}, Races: {races}")
    return races


def main(part):
    races = load_data(part)
    win_max = []
    for race in races:
        wins = race.trials()
        win_max.append(wins)
        logging.debug(f"{wins}")
    logging.debug(win_max)
    win_ways = functools.reduce(operator.mul, win_max, 1)
    logging.info(f"Part One Answer: {win_ways}")


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
