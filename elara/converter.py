import json
from pprint import pprint
from jinja2 import FileSystemLoader, Environment, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates"),
    auto_reload=False,
    autoescape=select_autoescape(),
)

template = env.get_template("export.html")
print(template.render(title="hello"))

with open("./sample.ipynb") as f:
    pprint(json.load(f)["metadata"])
