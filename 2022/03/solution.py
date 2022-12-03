from typing import List

if __name__ == "__main__":
    with open("input") as f:
        inf = f.read()

    rucksacks: List[str] = inf.split("\n")
    total_1: int = 0
    for r in rucksacks:
        c1: str = r[: int(len(r) / 2)]
        c2: str = r[int(len(r) / 2) :]
        common: str = list(set(c1).intersection(set(c2)))[0]
        is_upper: bool = common.isupper()
        val: int = ord(common.lower()) - 96
        if is_upper:
            val += 26
        total_1 += val
    print(total_1)

    total_2: int = 0
    for r in range(0, len(rucksacks), 3):
        r1: str
        r2: str
        r3: str
        r1, r2, r3 = rucksacks[r : r + 3]
        common: str = list(set(r1).intersection(set(r2), set(r3)))[0]
        is_upper: bool = common.isupper()
        val: int = ord(common.lower()) - 96
        if is_upper:
            val += 26
        total_2 += val
    print(total_2)
