import argparse
import logging


from typing import List
from dataclasses import dataclass, field


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


@dataclass
class Coordinate:
    x: int
    y: int

    def is_adjacent(self, coord) -> bool:
        delta_x = coord.x - self.x
        delta_y = coord.y - self.y
        logging.debug(
            "Checking adjacency: "
            f"({coord.x}, {coord.y}), ({self.x}, {self.y}); "
            f"delta: ({delta_x}, {delta_y})"
        )
        return (-1 <= delta_x <= 1) and (-1 <= delta_y <= 1)


@dataclass
class PartNumber:
    start: Coordinate
    end: Coordinate
    value: int

    def span(self) -> List[Coordinate]:
        span_x: int = self.end.x - self.start.x
        return [
            Coordinate(x=self.start.x + s, y=self.start.y) for s in range(span_x + 1)
        ]

    def adjacent_symbol_range(self, max_x: int, max_y: int) -> List[Coordinate]:
        low_x = self.start.x - 1 if self.start.x > 0 else self.start.x
        high_x = self.end.x + 1 if self.end.x + 1 < max_x else self.end.x

        low_y = self.start.y - 1 if self.start.y > 0 else self.start.y
        high_y = self.end.y + 1 if self.end.y + 1 < max_y else self.end.y

        adjacents = []
        for y in range(low_y, high_y + 1):
            for x in range(low_x, high_x + 1):
                adjacents.append(Coordinate(x, y))
        return adjacents


@dataclass
class Symbol:
    coord: Coordinate
    value: str

    def is_adjacent(self, span: List[Coordinate]) -> bool:
        adjacency = [c.is_adjacent(self.coord) for c in span]
        return any(adjacency)


@dataclass
class Schematic:
    symbols: List[Symbol] = field(default_factory=list)
    part_numbers: List[PartNumber] = field(default_factory=list)


def parse(matrix: List[List[str]]) -> Schematic:
    schematic = Schematic()
    for y, r in enumerate(matrix):
        curr_x = 0
        for x, c in enumerate(r):
            if curr_x > x:
                continue
            coord = Coordinate(x, y)
            if c == ".":
                continue
            if c not in "1234567890":
                s = Symbol(coord=coord, value=c)
                logging.debug(f"Storing: {s}")
                schematic.symbols.append(s)
            else:
                n = c
                temp_x = x
                start = coord
                end = coord
                while "".join(r[x : temp_x + 1]).isdigit() and temp_x + 1 <= len(r):
                    n = "".join(r[x : temp_x + 1])
                    logging.debug(f"Checking n: {n} at ({temp_x},{y})")
                    end = Coordinate(temp_x, y)
                    temp_x += 1
                curr_x = temp_x
                pn = PartNumber(start=start, end=end, value=int(n))
                logging.debug(f"Storing: {pn}")
                schematic.part_numbers.append(pn)

    return schematic


def main(part):
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    matrix = []
    for r in inf:
        matrix.append([_ for _ in r])
    max_y = len(matrix)
    max_x = len(matrix[0])
    total_pn = 0
    logging.debug(matrix)
    schematic = parse(matrix)
    logging.debug(schematic)
    for pn in schematic.part_numbers:
        adjacents = pn.adjacent_symbol_range(max_x, max_y)
        for c in adjacents:
            adjacent_value = matrix[c.y][c.x]
            if adjacent_value not in "1234567890.":
                logging.debug(f"Part Number: {pn.value}, Adjacent: {adjacent_value}")
                total_pn += pn.value

    logging.info(f"Part One Answer: {total_pn}")
    logging.info("Part Two Answer: ")


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
