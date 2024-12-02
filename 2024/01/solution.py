import bisect
import argparse
import logging
from typing import List, Tuple
from dataclasses import dataclass, field


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


def main(part: int):
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    left: List[int] = []
    right: List[int] = []

    for row in inf:
        l, r = row.split()
        left.append(int(l))
        right.append(int(r))
    left.sort()
    right.sort()

    sol: List[int] = []
    for idx, loc in enumerate(left):
        sol.append(abs(loc - right[idx]))
    logging.info(sol)
    result = sum(sol)

    logging.info(f"Part {'One' if part == 1 else 'Two'} Answer: {result}")


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
