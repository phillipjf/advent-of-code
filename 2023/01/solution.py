import re
import logging
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s",
)

if __name__ == "__main__":
    with open("input") as f:
        inf: str = f.read()

    cal_vals: List[str] = inf.split("\n")

    cal_nums = []
    for cn in cal_vals:
        cal_opts = str(re.sub(r"\D", "", cn))
        if len(cal_opts) > 1:
            cal_num = int(f"{cal_opts[0]}{cal_opts[-1]}")
        else:
            cal_num = int(f"{cal_opts}{cal_opts}")
        cal_nums.append(cal_num)
        logging.debug(f"{cn}: {cal_num}")
    logging.debug(cal_nums)
    logging.info(f"Answer: {sum(cal_nums)}")
