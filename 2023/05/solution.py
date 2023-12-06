import argparse
import logging


from typing import List, Optional
from dataclasses import dataclass, field


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


def kebab_to_snake(s: str) -> str:
    s = "_".join(s.split("-"))
    s = "_".join(s.split(" "))
    return s


@dataclass
class Seed:
    seed: int
    soil: Optional[int] = None
    fertilizer: Optional[int] = None
    water: Optional[int] = None
    light: Optional[int] = None
    temperature: Optional[int] = None
    humidity: Optional[int] = None
    location: Optional[int] = None


@dataclass
class Lookup:
    src: int
    dst: int
    range: int

    def check_src_range(self, check_val: int) -> bool:
        return check_val in range(self.src, self.src + self.range)

    def get_dst_val(self, check_val: int) -> int:
        offset = check_val - self.src
        return self.dst + offset


@dataclass
class Map:
    src_type: str
    dst_type: str
    lookups: List[Lookup] = field(default_factory=list)

    def lookup(self, lookup_value: int) -> int:
        for lu in self.lookups:
            if lu.check_src_range(lookup_value):
                return lu.get_dst_val(lookup_value)
        return lookup_value


@dataclass
class Almanac:
    seeds: List[Seed] = field(default_factory=list)
    seed_info: List[int] = field(default_factory=list)
    seed_to_soil_map: Optional[Map] = None
    soil_to_fertilizer_map: Optional[Map] = None
    fertilizer_to_water_map: Optional[Map] = None
    water_to_light_map: Optional[Map] = None
    light_to_temperature_map: Optional[Map] = None
    temperature_to_humidity_map: Optional[Map] = None
    humidity_to_location_map: Optional[Map] = None

    def maps(self) -> List[str]:
        return [
            "seed_to_soil_map",
            "soil_to_fertilizer_map",
            "fertilizer_to_water_map",
            "water_to_light_map",
            "light_to_temperature_map",
            "temperature_to_humidity_map",
            "humidity_to_location_map",
        ]


def load_data(part) -> Almanac:
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    almanac = Almanac()
    curr_map = ""
    for rn, r in enumerate(inf):
        if rn == 0:
            if part == 2:
                almanac.seed_info = [int(s) for s in r.split(": ")[1].split(" ")]
            else:
                almanac.seeds = [Seed(int(s)) for s in r.split(": ")[1].split(" ")]
        elif r == "":
            continue
        elif " map:" in r:
            title = kebab_to_snake(r).replace(":", "")
            curr_map = title
            src_type, dst_type = r.split(" ")[0].split("-to-")
            almanac.__setattr__(title, Map(src_type, dst_type))
        else:
            dst_range, src_range, range_len = [int(_) for _ in r.split(" ")]
            lookup = Lookup(src=src_range, dst=dst_range, range=range_len)
            m: Map = almanac.__getattribute__(curr_map)
            m.lookups.append(lookup)
    return almanac


def main(part):
    almanac = load_data(part)
    logging.debug(almanac)

    if part == 1:
        for seed in almanac.seeds:
            for map_type in almanac.maps():
                lookup_map: Map = almanac.__getattribute__(map_type)
                src_value = seed.__getattribute__(lookup_map.src_type)
                dst_value = lookup_map.lookup(src_value)
                seed.__setattr__(lookup_map.dst_type, dst_value)
            logging.debug(f"Seed {seed}")
        locs = sorted([s.location for s in almanac.seeds])[0]
        logging.info(f"Part One Answer: {locs}")

    if part == 2:
        locs = []
        seed_info = almanac.seed_info
        starts = seed_info[0::2]
        lengths = seed_info[1::2]
        for i in range(int(len(seed_info) / 2)):
            start = starts[i]
            end = start + lengths[i]
            for s in range(start, end):
                seed = Seed(s)
                for map_type in almanac.maps():
                    lookup_map: Map = almanac.__getattribute__(map_type)
                    src_value = seed.__getattribute__(lookup_map.src_type)
                    dst_value = lookup_map.lookup(src_value)
                    seed.__setattr__(lookup_map.dst_type, dst_value)
                logging.debug(f"Seed {seed}")
                locs.append(seed.location)
        close_loc = sorted(locs)[0]
        logging.info(f"Part Two Answer: {close_loc}")


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
