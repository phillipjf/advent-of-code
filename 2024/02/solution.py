import argparse
import logging
from typing import List, Tuple
from dataclasses import dataclass, field


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


def check_report(report, part, recheck) -> bool:
    first_step: bool = None
    report_errors: List[int] = []
    logging.info(f"Report: {report}; Recheck: {recheck}")

    for idx, level in enumerate(report):
        if idx + 1 >= len(report):
            logging.info(f"End of report; Found errors at indexes: {report_errors}.")
            if part == 1:
                return len(report_errors) == 0

            if part == 2 and len(report_errors) > 0 and not recheck:
                # # TODO: Figure out how to track if the change in direction is the first level
                # new_safe = False
                # for report_error in report_errors:
                #     new_report = report.copy()
                #     logging.debug(
                #         f"Trying report by removing level {report_error}, ({new_report[report_error]})"
                #     )
                #     del new_report[report_error]
                #     new_safe = check_report(new_report, part, True)
                #     if new_safe:
                #         break
                # return new_safe
                new_safe = False
                for i, l in enumerate(report):
                    new_report = report.copy()
                    del new_report[i]
                    new_safe = check_report(new_report, part, True)
                    if new_safe:
                        break
                return new_safe

            else:
                return len(report_errors) == 0

        next_level = report[idx + 1]
        step = next_level >= level
        if first_step is None:
            logging.debug(f"First step: {'increasing' if step else 'decreasing'}")
            first_step = step

        if first_step != step:
            logging.debug(f"Invalid step change ({next_level},{level})!")
            report_errors.append(idx)
            report_errors.append(idx + 1)
        if not (1 <= abs(next_level - level) <= 3):
            logging.debug(
                f"Value change ({next_level},{level}) out of range: {abs(next_level-level)}"
            )
            report_errors.append(idx)
            report_errors.append(idx + 1)


def main(part: int):
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    reports: List[List[int]] = [[int(l) for l in r.split()] for r in inf]

    safe_count = 0
    for idx, report in enumerate(reports):
        safe = check_report(report, part, False)
        if safe:
            safe_count += 1
        logging.info(f"Safe reports: {safe_count}/{idx+1}, {safe}.\n")

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
