import argparse
import logging
from typing import List, Optional
from dataclasses import dataclass, field

logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


@dataclass
class Cardinal:
    name: str
    x: int
    y: int
    valid_pipes: List[str]


DIRECTIONS: List[Cardinal] = [
    Cardinal("NORTH", 0, -1, ["|", "7", "F"]),
    Cardinal("SOUTH", 0, 1, ["|", "L", "J"]),
    Cardinal("EAST", 1, 0, ["-", "J", "7"]),
    Cardinal("WEST", -1, 0, ["-", "L", "F"]),
]


@dataclass
class Tile:
    x: int
    y: int
    pipe: str

    def valid_directions(self) -> List[Cardinal]:
        match self.pipe:
            case "F":
                return [DIRECTIONS[1], DIRECTIONS[2]]
            case "J":
                return [DIRECTIONS[0], DIRECTIONS[3]]
            case "7":
                return [DIRECTIONS[1], DIRECTIONS[3]]
            case "L":
                return [DIRECTIONS[0], DIRECTIONS[2]]
            case "-":
                return [DIRECTIONS[2], DIRECTIONS[3]]
            case "|":
                return [DIRECTIONS[0], DIRECTIONS[1]]
            case "S":
                return DIRECTIONS


@dataclass
class Map:
    tiles: List[List[Tile]] = field(default_factory=list)
    start: Optional[Tile] = None

    def get_next(self, tile: Tile) -> List[Tile]:
        adj_tiles = []
        for d in tile.valid_directions():
            adj_tile = self.get_tile(tile.x + d.x, tile.y + d.y)
            logging.debug(
                f"Checking {adj_tile}, Valid options: {d.name} {d.valid_pipes}"
            )
            if adj_tile is not None and (adj_tile.pipe in d.valid_pipes):
                adj_tiles.append(adj_tile)
        return adj_tiles

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        try:
            tile = self.tiles[y][x]
        except IndexError:
            return None
        return tile

    def find_start(self):
        for y, r in enumerate(self.tiles):
            for x, c in enumerate(r):
                if c.pipe == "S":
                    self.start = Tile(x, y, c.pipe)
                    break
        logging.debug(f"Start: {self.start}")

    def print(self, explored):
        for r in self.tiles:
            r_disp = ""
            for c in r:
                if (c.x, c.y) in explored:
                    t = c.pipe
                    t = (
                        t.replace("|", "║")
                        .replace("-", "═")
                        .replace("7", "╗")
                        .replace("F", "╔")
                        .replace("L", "╚")
                        .replace("J", "╝")
                    )
                    r_disp += t
                else:
                    r_disp += "."
            logging.info(r_disp)


def main(part):
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    tiles = [[t for t in r] for r in inf]
    pipe_map = Map()
    for y, r in enumerate(tiles):
        pipe_map.tiles.append([])
        for x, c in enumerate(r):
            pipe_map.tiles[y].append(Tile(x=x, y=y, pipe=c))

    pipe_map.find_start()
    path_len = 1
    curr_tile = pipe_map.start
    explored = []
    while True:
        curr_coor = (curr_tile.x, curr_tile.y)
        explored.append(curr_coor)
        next_tiles = [
            n for n in pipe_map.get_next(curr_tile) if (n.x, n.y) not in explored
        ]
        logging.debug(
            f"({path_len}) Current Tile: {curr_tile}, Next tiles: {next_tiles}"
        )
        if len(next_tiles) == 0:
            logging.debug("1. Broke here")
            break
        if path_len > 1 and curr_coor == (pipe_map.start.x, pipe_map.start.y):
            logging.debug("2. Broke here")
            break
        if len(next_tiles) > 1 and path_len != 1:
            raise Exception
        else:
            curr_tile = next_tiles[0]
        path_len += 1
    pipe_map.print(explored)
    logging.info(f"Part one answer: {int(path_len/2)}")


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
