from typing import List, Tuple, Callable, Dict, Any
from operator import iadd, isub


def update_tail(h_curr_pos: List[int], t_curr_pos: List[int]) -> List[int]:
    safe: List[List[int, int]] = [
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
    delta: List[int] = [abs(h_curr_pos[0] - t_curr_pos[0]),
                        abs(h_curr_pos[1] - t_curr_pos[1])]

    if delta in safe:
        return t_curr_pos
    if delta[0] > 1:
        if h_curr_pos[0] > t_curr_pos[0]:
            t_curr_pos[0] += 1
        else:
            t_curr_pos[0] -= 1
    if delta[1] > 1:
        if h_curr_pos[1] > t_curr_pos[1]:
            t_curr_pos[1] += 1
        else:
            t_curr_pos[1] -= 1
    if delta[1] > delta[0]:
        t_curr_pos[0] = h_curr_pos[0]
    if delta[0] > delta[1]:
        t_curr_pos[1] = h_curr_pos[1]
    return [t_curr_pos[0], t_curr_pos[1]]


def move(moves: List[str], rope_length: int) -> int:
    rope: List[List[int, int]] = [[0, 0] for _ in range(rope_length)]
    t_coords: List[Tuple[int, int]] = [(0, 0)]
    h_curr_pos: List[int] = [0, 0]

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
            h_curr_pos = rope[0]
            h_curr_pos[ind] = op(h_curr_pos[ind], 1)

            for i in range(len(rope)-1):
                k_curr_pos = update_tail(rope[i], rope[i+1])
                rope[i+1] = k_curr_pos
            t_coords.append(tuple(rope[len(rope)-1]))
    return len(set(t_coords))


if __name__ == "__main__":
    with open("input") as f:
        inf = f.read()

    moves = inf.split("\n")

    print(move(moves, 2))
    print(move(moves, 10))
