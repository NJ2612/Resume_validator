import os
import json
from validator import validate_resume


INPUT_FOLDER = "inputs"
OUTPUT_FOLDER = "output"


def run_pipeline():

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for file in os.listdir(INPUT_FOLDER):

        if file.endswith(".json"):

            input_path = os.path.join(INPUT_FOLDER, file)

            with open(input_path, "r") as f:
                data = json.load(f)

            result = validate_resume(data)

            output_file = file.replace(".json", "_output.json")
            output_path = os.path.join(OUTPUT_FOLDER, output_file)

            with open(output_path, "w") as f:
                json.dump(result, f, indent=4)

            print(f"Processed: {file}")


if __name__ == "__main__":
    run_pipeline()