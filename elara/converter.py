import json
from pprint import pprint

with open("./sample.ipynb") as f:
    pprint(json.load(f)["metadata"])
