import re
import argparse
import logging
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


def swap(m: str) -> int:
    match m:
        case "one":
            return 1
        case "two":
            return 2
        case "three":
            return 3
        case "four":
            return 4
        case "five":
            return 5
        case "six":
            return 6
        case "seven":
            return 7
        case "eight":
            return 8
        case "nine":
            return 9
    return int(m)


def main(part):
    with open("input") as f:
        inf: str = f.read()

    cal_vals: List[str] = inf.split("\n")
    cal_nums: List[int] = []

    if part == 1:
        m = re.compile(r"(?=(\d))")
    elif part == 2:
        m = re.compile(r"(?=(one|two|three|four|five|six|seven|eight|nine|\d))")
    else:
        logging.error("Invalid part.")
        return 1

    for cn in cal_vals:
        cal_opts = m.findall(cn)
        if part == 2:
            cal_opts = [swap(vv) for vv in cal_opts]

        if len(cal_opts) > 1:
            cal_num = int(f"{cal_opts[0]}{cal_opts[-1]}")
        else:
            cal_num = int(f"{cal_opts[0]}{cal_opts[0]}")
        cal_nums.append(cal_num)
        logging.debug(f"{cn}: {cal_num}")
    logging.debug(cal_nums)
    logging.info(f"Answer: {sum(cal_nums)}")


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
