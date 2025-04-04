from jinja2 import FileSystemLoader, Environment, select_autoescape
from dataclasses import dataclass

from elara.models import Notebook


@dataclass(frozen=True)
class RenderOptions:
    filename: str
    notebook: Notebook
    # todo styles


class TemplateRenderer:
    def __init__(self):
        self.__env = Environment(
            loader=FileSystemLoader("templates"),
            auto_reload=False,
            autoescape=select_autoescape(),
        )

        self.__template = self.__env.get_template("export.html")

    def render(self, options: RenderOptions):
        return self.__template.render(**options.as_dict())
