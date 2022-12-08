from typing import List


def scenic_value(trees: List[int], curr_tree: int) -> int:
    """
    Calculate the 'scenic value' from the perspective of a tree looking out
    in one single direction (up, down, left, right). The 'scenic value' is the
    count of trees visible. A tree is visible if its value is less than the
    'current tree' up to (inclusive of) the first tree with a value greater
    than or equal to the 'current tree'.

    trees: list of tree values in one direction from the perspective of curr_tree
    curr_tree: the tree value of a current tree (the tree to consider perspective from)

    returns: integer sum of trees visible from curr_tree
    """
    scenic_value: int = 0
    # iterate over the visible trees in one direction
    for t in trees:
        # if the tree value is greater than the current tree
        if t >= curr_tree:
            # increment the scenic_value as it is inclusive
            scenic_value += 1
            break
        else:
            # otherwise the tree is 'visible' and increment scenic_value
            scenic_value += 1
    return scenic_value


if __name__ == "__main__":
    with open("input") as f:
        inf: str = f.read()

    trees: List[str] = inf.split("\n")
    total_visible: int = 0
    scenic_scores: List[int] = []
    x: int
    y: int
    row: str
    col: str

    for y, row in enumerate(trees):
        for x, col in enumerate(row):
            # using trees[y][x] is more clear than using row[x] to access
            # the trees matrix
            curr_tree: int = int(trees[y][x])

            # convert each tree value in the y row to an int
            tree_row: List[int] = [int(t) for t in trees[y]]
            # grab each tree value in the x column and convert to int
            tree_col: List[int] = [int(t[x]) for t in trees]

            # slice the row by left/right and
            # and the column by up/down excluding the current tree
            tree_left: List[int] = tree_row[:x]
            tree_right: List[int] = tree_row[x + 1 :]
            tree_up: List[int] = tree_col[:y]
            tree_down: List[int] = tree_col[y + 1 :]

            # identify the max value in the left/right, up/down lists
            # if the list is empty (an edge tree), use an out-of-bounds
            # value (-1) to ensure later comparison is valid
            max_left = max(tree_left, default=-1)
            max_right = max(tree_right, default=-1)
            max_up = max(tree_up, default=-1)
            max_down = max(tree_down, default=-1)

            # if any of the max tree values in any direction are less than
            # the current tree value, the tree is visible form that direction
            visible = any(
                [
                    max_left < curr_tree,
                    max_right < curr_tree,
                    max_up < curr_tree,
                    max_down < curr_tree,
                ]
            )
            if visible:
                total_visible += 1

            # part two
            # compute the scenic value for each of the left/right, up/down lists
            # keep in mind: order is important. looking out from the tree,
            # left and up will be reversed.
            scenic_left: int = scenic_value(list(reversed(tree_left)), curr_tree)
            scenic_right: int = scenic_value(tree_right, curr_tree)
            scenic_up: int = scenic_value(list(reversed(tree_up)), curr_tree)
            scenic_down: int = scenic_value(tree_down, curr_tree)

            # the total scenic score is the product of each direction's scenic value
            total_scenic_score = scenic_left * scenic_right * scenic_up * scenic_down

            # compile a list of scenic scores for each tree position
            scenic_scores.append(total_scenic_score)

            # # debug info line for each tree
            # print(
            #     f"({x}:{y}) "
            #     f"[{scenic_left}*{scenic_right}*{scenic_up}*{scenic_down}"
            #     f"={total_scenic_score}] "
            #     f"({total_visible}) {visible}: {curr_tree} "
            #     f"| L: {max_left}({max_left<curr_tree}), "
            #     f"R: {max_right}({max_right<curr_tree}), "
            #     f"U: {max_up}({max_up<curr_tree}), "
            #     f"D: {max_down}({max_down<curr_tree})"
            # )

    print("Total Visible Trees:", total_visible)
    print("Highest Scenic Score:", max(scenic_scores))
