import argparse
import logging
from typing import List, Dict, Tuple
import math
from time import sleep

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


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


def part_one(instructions: str, nodes: Dict[str, Tuple[str, str]]):
    start: str = "AAA"
    end: str = "ZZZ"
    steps: int = 0

    curr_node = start
    while curr_node != end:
        logging.debug(f"Current Node: {curr_node}")
        for i in instructions:
            logging.debug(f"Going {'L' if i == '0' else 'R'}...")
            steps += 1
            curr_node = nodes[curr_node][int(i)]
            logging.debug(f"Next node: {curr_node}")
            if curr_node == end:
                break
    logging.info(f"Part One Answer: {steps}")


def part_two_ish(
    instructions: str,
    nodes: Dict[str, Tuple[str, str]],
    start: str,
) -> int:
    steps: int = 0

    curr_node = start
    while not curr_node.endswith("Z"):
        logging.debug(f"Current Node: {curr_node}")
        for i in instructions:
            logging.debug(f"Going {'L' if i == '0' else 'R'}...")
            steps += 1
            curr_node = nodes[curr_node][int(i)]
            logging.debug(f"Next node: {curr_node}")
            if curr_node.endswith("Z"):
                break
    logging.info(f"Part Two-ish Answer: {steps}")
    return steps


def part_two(instructions: str, nodes: Dict[str, Tuple[str, str]]):
    start: Dict[str, Tuple[str, str]] = {
        n: v for n, v in nodes.items() if n.endswith("A")
    }

    steps: int = 0
    logging.debug(f"Instructions: {instructions}")
    all_next_keys: bool = False
    while not all_next_keys:
        for inst in instructions:
            next_nodes = {}
            logging.debug(f"Going {'L' if inst == '0' else 'R'}...")
            steps += 1
            for c, v in start.items():
                next_node = v[int(inst)]
                logging.debug(f"Current Node -> Next node: {c} -> {next_node}")
                next_nodes[next_node] = nodes[next_node]
            start = next_nodes
            next_keys = [k for k in start.keys()]
            all_next_keys = all([k.endswith("Z") for k in next_keys])
            if steps % 100000 == 0:
                logging.info(
                    f"Steps: {steps}, Next Keys: ({all_next_keys}) {next_keys}"
                )
            if all_next_keys:
                break
    logging.info(f"Part Two Answer: {steps}")


def main(part):
    instructions, nodes = load_data()
    instructions = instructions.replace("R", "1").replace("L", "0")
    if part == 1:
        part_one(instructions, nodes)
    if part == 2:
        part_two(instructions, nodes)
    if part == 3:
        start: Dict[str, Tuple[str, str]] = {
            n: v for n, v in nodes.items() if n.endswith("A")
        }
        results = []
        for n in start.keys():
            logging.info(f"Checking {n}...")
            r = part_two_ish(instructions, nodes, n)
            results.append(r)
        result = math.lcm(*results)
        logging.info(f"Part Two-ish Answer Answer: {result}, {results}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "part",
        metavar="P",
        type=int,
        choices=[1, 2, 3],
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
