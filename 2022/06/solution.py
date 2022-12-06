if __name__ == "__main__":
    with open("input") as f:
        inf = f.read()

    # Solution 1
    for i in range(len(inf)):
        if len(set(inf[i : i + 4])) == 4:
            print(i + 4)  # offset for start-of-packet marker
            break

    # Solution 2
    for i in range(len(inf)):
        if len(set(inf[i : i + 14])) == 14:
            print(i + 14)  # offset for start-of-packet marker
            break
