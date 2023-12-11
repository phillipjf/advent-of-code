import argparse
import logging
from typing import List


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


def uni_print(universe):
    for r in universe:
        logging.debug("".join(r))
    logging.debug("")


def expand_universe(universe):
    # uni_print(universe)
    expanded_universe = []
    for r in universe:
        expanded_universe.append(r.copy())
        if all([c == "." for c in r]):
            expanded_universe.append(r.copy())
    # uni_print(expanded_universe)
    offset = 0
    for c in range(len(universe[0])):
        if all([universe[r][c] == "." for r in range(len(universe))]):
            for r in expanded_universe:
                r.insert(c + offset, ".")
            offset += 1
    # uni_print(expanded_universe)
    return expanded_universe


def main(part):
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    universe = [[c for c in r] for r in inf]
    universe = expand_universe(universe)

    galaxies = []
    for r, rv in enumerate(universe):
        for c, cv in enumerate(rv):
            if cv == "#":
                galaxies.append((c, r))
    logging.debug(f"Galaxies: {galaxies}")

    pairs = []
    for galaxy_a in galaxies:
        for galaxy_b in galaxies:
            if (
                ((galaxy_a, galaxy_b) not in pairs)
                and ((galaxy_b, galaxy_a) not in pairs)
                and (galaxy_a != galaxy_b)
            ):
                pairs.append((galaxy_a, galaxy_b))
    logging.debug(f"Pairs: {len(pairs)}; {pairs}")
    dists = []
    for pair in pairs:
        dist = abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
        dists.append(dist)
        logging.debug(f"Distance {pair}: {dist}")
    answer = sum(dists)
    # logging.debug(f"Dists: {answer}; {dists}")
    logging.info(f"Part {'One' if part ==1 else 'Two'} Answer: {answer}")


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
