import json

level_array: list
rows: int
columns: int


def load_to_list(level: int) -> json:
    global level_array, rows, columns
    PATH = "./levels/" + str(level) + ".json"
    with open(PATH) as f:
        data = json.load(f)
    return data


# testing purpose
def main():
    load_to_list(1)
    print(level_array)


if __name__ == "__main__":
    main()
