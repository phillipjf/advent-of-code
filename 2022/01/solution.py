from typing import List


if __name__ == "__main__":
    elve_totals: List[int] = []
    max_cal: int = 0
    with open("input") as f:
        inf = f.read()
    elves: List[str] = inf.split("\n\n")
    # print(f"Total Elves: {len(elves)}")
    elve: str
    for elve in elves:
        elve_list: List = elve.strip().split("\n")
        # print(f"Elve: {elve_list}")
        elve_sum: int = 0
        for c in elve_list:
            elve_sum += int(c)
        elve_totals.append(elve_sum)
        if elve_sum > max_cal:
            max_cal = elve_sum
        # print(f"Elve Sum: {elve_sum}")
    print(f"Max Cal: {max_cal}")
    print(f"Max: {max(elve_totals)}")
    print(f"Top 3: {sorted(elve_totals, reverse=True)[0:3]}")
    print(f"Sum Top 3: {sum(sorted(elve_totals,reverse=True)[0:3])}")
