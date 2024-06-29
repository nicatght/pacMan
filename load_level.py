import json

level_array = None
level: int
rows: int
columns: int
point: int


def load_level(s_level: int) -> None:
    global level_array, rows, columns, level, point
    level = s_level
    PATH = "./levels/" + str(s_level) + ".json"
    with open(PATH) as f:
        data = json.load(f)
        level_array = data["data"]
        rows = data["rows"]
        columns = data["columns"]

    point = 0
    # load point
    for i in level_array:
        if i == 0:
            point += 1


def load_data():
    return level_array


# testing purpose
def main():
    load_level(1)
    print(level_array)


if __name__ == "__main__":
    main()
