import argparse
import logging
from typing import List
from dataclasses import dataclass


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


@dataclass
class Node:
    name: str
    l_ele: str
    r_ele: str


def load_data():
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    instructions = ""
    nodes = {}
    for i, l in enumerate(inf):
        if i == 0:
            instructions = l
            continue
        if l == "":
            continue
        else:
            name, eles = l.split(" = ")
            l_ele, r_ele = eles.strip("()").split(", ")
            nodes[name] = (l_ele, r_ele)
    return instructions, nodes


def main(part):
    instructions, nodes = load_data()
    instructions = instructions.replace("R", "1").replace("L", "0")
    start = "AAA"
    end = "ZZZ"
    steps = 0

    curr_node = start
    while curr_node != end:
        logging.debug(f"Current Node: {curr_node}")
        for i in instructions:
            logging.debug(f"Going {'L' if i == 0 else 'R'}...")
            steps += 1
            curr_node = nodes[curr_node][int(i)]
            logging.debug(f"Next node: {curr_node}")
            if curr_node == end:
                break
    logging.info(f"Part One Answer: {steps}")


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
