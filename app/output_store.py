import json
from pathlib import Path

BASE_DIRECTORY = Path(__file__).resolve().parent.parent

FILE_PATH = BASE_DIRECTORY / "data" / "generated_outputs.json"


def save_output(selection_id, output):

    with open(FILE_PATH, "r") as file:
        data = json.load(file)

    generated = {
        "id": len(data) + 1,
        "selection_id": selection_id,
        "output": output
    }

    data.append(generated)

    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

    return generated