from typing import List, Dict, Any, Callable

import operator

MAX_SIZE: int = 100000
TOTAL_FILESYSTEM: int = 70000000
TOTAL_UNUSED_NEEDED: int = 30000000


def walk(tree: Dict, op: Callable, size: int):
    for k, v in tree.items():
        if isinstance(v, dict):
            for p in walk(v, op, size):
                yield (k, *p)
        else:
            if op(int(v), size):
                yield (k, v)


if __name__ == "__main__":
    with open("input") as f:
        inf: str = f.read()

    terminal_output: List[str] = inf.split("\n")

    file_tree: Dict[str, Any] = {}
    # keep track of where we are in the tree
    current_path: List[str] = []
    output_line: str
    for output_line in terminal_output:
        parsed_line: List[str] = output_line.split(" ")
        if parsed_line[0] == "$":
            # only two commands: 'cd' and 'ls
            if parsed_line[1] == "cd":
                # either move up the tree ('..') or into a dir
                # no 'cd' is more than one dir (ex: 'foo/bar')
                if parsed_line[2] == "..":
                    # move up one dir
                    current_path.pop()
                else:
                    # traverse the tree
                    tmp = file_tree
                    for d in current_path:
                        tmp = tmp[d]

                    if not tmp.get(parsed_line[2]):
                        # if this is the first time in this dir,
                        # initialize the total size
                        tmp[parsed_line[2]] = {"total_size": 0}
                    # update our current path to include the new dir
                    current_path.append(parsed_line[2])
            elif parsed_line[1] == "ls":
                # we don't care about 'ls' command, just the output
                ...
        elif parsed_line[0] == "dir":
            # if the output is a dir, traverse the tree to that location
            tmp = file_tree
            for d in current_path:
                tmp = tmp[d]
            # if the dir has not been visited before,
            # initialize the 'total_size' attr
            if not tmp.get(parsed_line[1]):
                tmp[parsed_line[1]] = {"total_size": 0}
        else:
            # lastly, we are looking at a file, so traverse the tree
            tmp = file_tree
            for d in current_path:
                tmp = tmp[d]
                # add the file size to each of the dirs in the tree
                tmp["total_size"] += int(parsed_line[0])
            # # we don't care about the actual files in this but if we did,
            # # we could add them to the dir via:
            # tmp[parsed_line[1]] = parsed_line[0]

    total_under_max_size: int = 0
    # traverse the entire file tree and find all dirs under the MAX_SIZE
    for p in walk(file_tree, operator.lt, MAX_SIZE):
        total_under_max_size += int(p[-1:][0])
    print(f"Total Under {MAX_SIZE}: {total_under_max_size}")

    total_used = file_tree["/"]["total_size"]
    total_available = TOTAL_FILESYSTEM - total_used
    total_needed = TOTAL_UNUSED_NEEDED - total_available
    print(f"Total Used: {total_used}")
    print(f"Total Available: {total_available}")
    print(f"Total Needed: {total_needed}")

    # traverse the entire file tree and find all dirs over the total_needed,
    # sort, and return the smallest size.
    closest = sorted([p[-1:][0] for p in walk(file_tree, operator.ge, total_needed)])[0]
    print(f"Smallest directory to delete: {closest}")
