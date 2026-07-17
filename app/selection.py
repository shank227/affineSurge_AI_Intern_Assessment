import json
from pathlib import Path

BASE_DIRECTORY = Path(__file__).resolve().parent.parent
FILE_PATH = BASE_DIRECTORY / "data" / "selections.json"


def save_selection(name, version, node_ids):

    with open(FILE_PATH, "r") as file:
        data = json.load(file)

    selection = {
        "id": len(data) + 1,
        "name": name,
        "version": version,
        "node_ids": node_ids
    }

    data.append(selection)

    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

    return selection