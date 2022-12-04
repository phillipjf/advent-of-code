from typing import List

if __name__ == "__main__":
    with open("input") as f:
        inf = f.read()

    total_1: int = 0
    total_2: int = 0
    pairs: List[str] = inf.split("\n")
    for p in pairs:
        e1: str
        e2: str
        e1, e2 = p.split(",")
        e1r1: str
        e1r2: str
        e2r1: str
        e2r2: str
        e1r1, e1r2 = e1.split("-")
        e2r1, e2r2 = e2.split("-")

        e1r: set = set(range(int(e1r1), int(e1r2) + 1))
        e2r: set = set(range(int(e2r1), int(e2r2) + 1))

        if e1r.issubset(e2r) or e1r.issuperset(e2r):
            total_1 += 1
        if e1r.intersection(e2r):
            total_2 += 1
    print(total_1)
    print(total_2)
