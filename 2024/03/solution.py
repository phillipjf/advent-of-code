import re
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
        inf: str = f.read()

    solution: int = 0
    pattern = re.compile(r"mul\((?P<op1>\d{1,3}),(?P<op2>\d{1,3})\)")
    matches: List[Tuple] = pattern.findall(inf)
    for match in matches:
        op1, op2 = match
        product: int = int(op1) * int(op2)
        logging.debug(f"Adding product of {op1}*{op2}={product}")
        solution += product
    logging.info(f"Part {'One' if part ==1 else 'Two'} Answer: {solution}")


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
