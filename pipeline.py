import os
import json

from config import INPUT_FOLDER, OUTPUT_FOLDER
from validator.engine import validate_resume


def run_pipeline():

    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print("Input folder created. Add JSON resumes inside.")
        return

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for file in os.listdir(INPUT_FOLDER):

        if not file.endswith(".json"):
            continue

        input_path = os.path.join(INPUT_FOLDER, file)

        try:
            with open(input_path, "r") as f:
                data = json.load(f)

        except Exception:
            print(f"Skipping invalid JSON: {file}")
            continue

        result = validate_resume(data)

        output_file = file.replace(".json", "_validated.json")
        output_path = os.path.join(OUTPUT_FOLDER, output_file)

        with open(output_path, "w") as f:
            json.dump(result, f, indent=4)

        print(f"Processed: {file}")


if __name__ == "__main__":
    run_pipeline()