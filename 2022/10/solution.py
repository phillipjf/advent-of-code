if __name__ == '__main__':
    with open('input') as f:
        inf = f.read()

    instructions = inf.split('\n')

    X: int = 1
    cycle: int = 0
    instruction_cycles = {
        "noop": 1,
        "addx": 2
    }
    crt: str = ""
    total: int = 0
    for instruction in instructions:
        parse = instruction.split(" ")
        inst = parse[0]
        if len(parse) > 1:
            param = int(parse[1])
        else:
            param = None

        for i in range(instruction_cycles[inst]):
            cycle += 1
            if cycle % 20 == 0:
                if cycle in [20, 60, 100, 140, 180, 220]:
                    print(f"{cycle}: ({X}) - {cycle * X}")
                    total += cycle*X
            if cycle % 40 in [X, X+1, X+2]:
                crt += "#"
            else:
                crt += "."
        if param:
            X += param
    print(total)
    for i in range(0, len(crt), 40):
        print(f'{i:<3} {crt[i:i+40]}')
