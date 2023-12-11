import argparse
import logging
from typing import List, Tuple


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


def move_galaxies(universe: List[str], galaxies: List[Tuple[int, int]], append: int):
    logging.info("Expanding universe rows...")
    y_offset = 0
    for r, rv in enumerate(universe):
        if all([c == "." for c in rv]):
            logging.debug(f"Found empty row: {r}")
            for i, galaxy in enumerate(galaxies):
                if galaxy[1] > r + y_offset:
                    new_coords = (galaxy[0], galaxy[1] + append)
                    logging.debug(f"Moving {galaxy} -> {new_coords}")
                    galaxies[i] = new_coords
            y_offset += append
    logging.info("Expanding universe rows...complete.")

    logging.info("Expanding universe cols...")
    x_offset = 0
    for c in range(len(universe[0])):
        if all([universe[r][c] == "." for r in range(len(universe))]):
            logging.debug(f"Found empty col: {c}")
            for i, galaxy in enumerate(galaxies):
                if galaxy[0] > c + x_offset:
                    new_coords = (galaxy[0] + append, galaxy[1])
                    logging.debug(f"Moving {galaxy} -> {new_coords}")
                    galaxies[i] = new_coords
            x_offset += append
    logging.info("Expanding universe cols...complete.")

    return galaxies


def main(part):
    with open("input") as f:
        universe: List[str] = f.read().splitlines()

    growth_factor: int = 1 if part == 1 else 999999

    logging.info("Finding galaxies...")
    galaxies = []
    for r, rv in enumerate(universe):
        for c, cv in enumerate(rv):
            if cv == "#":
                galaxies.append((c, r))
    logging.debug(f"Galaxies: {galaxies}")
    logging.info("Finding galaxies...complete")

    logging.info("Expanding universe...")
    galaxies = move_galaxies(universe, galaxies, growth_factor)
    logging.info("Expanding universe...complete.")

    logging.info("Building pairs...")
    pairs = [
        (galaxy_a, galaxy_b)
        for i, galaxy_a in enumerate(galaxies)
        for galaxy_b in galaxies[i + 1 :]
    ]
    logging.debug(f"Pairs: {len(pairs)}; {pairs}")
    logging.info("Building pairs...complete")

    logging.info("Calculating distances...")
    dists = []
    for pair in pairs:
        dist = abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1])
        dists.append(dist)
        logging.debug(f"Distance {pair}: {dist}")
    logging.info("Calculating distances...complete")
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
