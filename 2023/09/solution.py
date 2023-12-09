import argparse
import logging
from typing import List


logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)


def calc(row: List[int], rows: List[List[int]]) -> List[List[int]]:
    if rows == []:
        rows.append(row)
    next_row = [row[i] - row[i - 1] for i in range(1, len(row))]
    rows.append(next_row)
    if not all([i == 0 for i in next_row]):
        logging.debug(f"Interim Rows: {rows}")
        return calc(next_row, rows)
    else:
        logging.debug(f"Interim Rows: {rows}")
        return rows


def main(part):
    with open("input") as f:
        inf: List[str] = f.read().splitlines()

    orig_rows = [[int(i) for i in l.split(" ")] for l in inf]
    logging.debug(f"Rows: {orig_rows}")
    final = []
    for r in orig_rows:
        logging.debug(f"Processing: {r}")
        t_rows = calc(r, [])
        logging.debug(f"Total Rows: {t_rows}")
        last_vals = []
        for i in reversed(range(len(t_rows))):
            r = t_rows[i][-1]
            if i == len(t_rows) - 1:
                last_vals.append(r)
                continue
            r_1 = last_vals[-1]
            last_vals.append(r + r_1)
            logging.debug(f"Val: {r}+{r_1}={r+r_1}")
        logging.debug(f"Last Values: {last_vals}")
        final.append(last_vals[-1])
    logging.debug(f"Finals: {final}")

    logging.info(f"Part One Answer: {sum(final)}")


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
