from typing import List, Tuple, Callable, Dict, Any
from operator import iadd, isub


def update_tail(h_curr_pos: List[int], t_curr_pos: List[int]) -> List[int]:
    t_new_pos: List[int] = []
    safe = [
        [0, 0],
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0],
        [1, 1],
        [-1, 1],
        [1, -1],
        [-1, -1],
    ]
    delta: List[int] = [h_curr_pos[0] - t_curr_pos[0], h_curr_pos[1] - t_curr_pos[1]]
    if delta in safe:
        return t_curr_pos
    elif 0 in delta:
        # if one delta is 0 and other is [2,-2], moving UDLR
        # make value [2,-2] [1,-1]
        if delta[0] in [2, -2]:
            if delta[0] > 0:
                delta[0] -= 1
            else:
                delta[0] += 1
            t_new_pos = [h_curr_pos[0] - delta[0], h_curr_pos[1] - delta[1]]
        elif delta[1] in [2, -2]:
            if delta[1] > 0:
                delta[1] -= 1
            else:
                delta[1] += 1
            t_new_pos = [h_curr_pos[0] - delta[0], h_curr_pos[1] - delta[1]]
        # if one delta is 0 and other is [1,-1], no move diagonal
        elif delta[0] in [1, -1] or delta[1] in [1, -1]:
            t_new_pos = t_curr_pos
        else:
            t_new_pos = t_curr_pos

    # if one delta is [1,-1] and other is [2,-2], move diagonal
    elif (delta[0] in [1, -1] and delta[1] in [2, -2]) or (
        delta[0] in [2, -2] and delta[1] in [1, -1]
    ):
        if delta[0] > 0:
            delta[0] -= 1
        else:
            delta[0] += 1
        if delta[1] > 0:
            delta[1] -= 1
        else:
            delta[1] += 1
        t_new_pos = [h_curr_pos[0] - delta[0], h_curr_pos[1] - delta[1]]

    else:
        raise Exception(f"Bad spot {delta}")
    return t_new_pos


if __name__ == "__main__":
    with open("input") as f:
        inf = f.read()

    moves = inf.split("\n")

    h_coords: List[Tuple[int, int]] = [(0, 0)]
    t_coords: List[Tuple[int, int]] = [(0, 0)]
    h_curr_pos: List[int] = [0, 0]
    t_curr_pos: List[int] = [0, 0]

    move_map: Dict[str, Dict[str, Any]] = {
        "U": {"op": iadd, "ind": 1},
        "D": {"op": isub, "ind": 1},
        "R": {"op": iadd, "ind": 0},
        "L": {"op": isub, "ind": 0},
    }

    for m in moves:
        _ = m.split(" ")
        dir: str = _[0]
        step: int = int(_[1])

        for i in range(step):
            ind: int = move_map[dir]["ind"]
            op: Callable = move_map[dir]["op"]
            h_curr_pos[ind] = op(h_curr_pos[ind], 1)
            h_coords.append(tuple(h_curr_pos))
            t_curr_pos = update_tail(h_curr_pos, t_curr_pos)
            t_coords.append(tuple(t_curr_pos))

            # print(
            #     f"{dir}|{step}.{i} "
            #     f"| h: {str(h_curr_pos):<8} "
            #     f"t: {str(t_curr_pos):<8} "
            #     f"d: {str([h_curr_pos[0] - t_curr_pos[0], h_curr_pos[1] - t_curr_pos[1]]):<8}"
            # )

    print(len(set(t_coords)))
