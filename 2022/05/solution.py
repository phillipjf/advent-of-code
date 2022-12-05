from typing import List

if __name__ == "__main__":
    with open("input") as f:
        inf = f.read()

    crates: str
    moves: str
    crates, moves = inf.split("\n\n")

    crate_columns: List[List[str]] = []
    crate_stacks: List[str] = crates.split("\n")
    for row in crate_stacks:
        col: int
        i: int
        for col, i in enumerate(range(0, len(row), 4)):
            try:
                crate_columns[col]
            except IndexError:
                crate_columns.append([])
            crate: str = row[i : i + 4].strip()
            if crate.startswith("["):  # Filter out empty slots and column labels
                crate_columns[col].append(crate)

    # ex: move 1 from 8 to 7
    move: str
    for move in moves.split("\n"):
        parse: List[str] = move.split(" ")
        count: int = int(parse[1])
        source: int = int(parse[3])
        dest: int = int(parse[5])
        # # Solution 1
        # for i in range(0, count):
        #     crate = crate_columns[source - 1].pop(0)
        #     crate_columns[dest - 1].insert(0, crate)

        # Solution 2
        crate_stack: List[str] = crate_columns[source - 1][0:count]
        del crate_columns[source - 1][0:count]
        crate_columns[dest - 1] = crate_stack + crate_columns[dest - 1]

    solution: str = ""
    c: List[str]
    for c in crate_columns:
        solution += c[0].strip("[]")

    print(solution)
