from dataclasses import asdict, dataclass
from datetime import date
from jinja2 import Environment, FileSystemLoader, select_autoescape

from elara.models import Notebook


@dataclass(frozen=True, slots=True)
class RenderOptions:
    filename: str
    notebook: Notebook
    date_: date = date.today()
    # todo styles

    def as_dict(self):
        return asdict(self)


class TemplateRenderer:
    def __init__(self):
        self.__env = Environment(
            loader=FileSystemLoader("templates"),
            auto_reload=False,
            autoescape=select_autoescape(),
        )

        self.__template = self.__env.get_template("export.html")

    def render(self, options: RenderOptions):
        return self.__template.render(
            filename=options.filename, date_=options.date_, notebook=options.notebook
        )
