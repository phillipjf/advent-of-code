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

    reports: List[List[int]] = [[int(l) for l in r.split()] for r in inf]

    safe_count = 0
    for report in reports:
        first_step: bool = None
        logging.debug(f"Report: {report}")
        for idx, level in enumerate(report):
            if idx + 1 >= len(report):
                logging.debug(f"End of report: {idx+1}, {len(report)}")
                safe_count += 1
                break
            next_level = report[idx + 1]
            step = next_level > level
            if first_step is None:
                logging.debug(f"First step: {'increasing' if step else 'decreasing'}")
                first_step = step
            elif first_step != step:
                logging.debug("Next step does not match first step!")
                break
            if not (1 <= abs(next_level - level) <= 3):
                logging.debug(f"Increase too large: {abs(next_level-level)}")
                break

    logging.info(f"Part {'One' if part ==1 else 'Two'} Answer: {safe_count}")


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
