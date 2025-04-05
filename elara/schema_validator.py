import importlib
import json
from typing import Any

from jsonschema import Draft4Validator, validate


def get_notebook_schema() -> dict[str, Any]:
    ref = importlib.resources.files("elara") / "schemas" / "v4.0.json"
    with importlib.resources.as_file(ref) as jsonschema_path:
        with open(str(jsonschema_path)) as f:
            return json.load(f)


notebook_schema = get_notebook_schema()


def validate_notebook(notebook_json: dict[str, Any]) -> bool:
    validate(notebook_json, notebook_schema, cls=Draft4Validator)


if __name__ == "__main__":
    import json

    with open("./sample.ipynb") as f:
        nb = json.load(f)
        print(validate_notebook(nb))
