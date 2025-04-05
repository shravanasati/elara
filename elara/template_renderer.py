from dataclasses import asdict, dataclass
from datetime import date
import re
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt

from elara.models import Notebook


@dataclass(frozen=True, slots=True)
class RenderOptions:
    filename: str
    notebook: Notebook
    date_: date = date.today()
    # todo styles

    def as_dict(self):
        return asdict(self)


def get_source(s: str | list[str]) -> str:
    """
    Jinja filter to render model `Source`.
    """
    if isinstance(s, str):
        return s
    elif isinstance(s, list):
        return "".join(s)
    raise ValueError(f"Invalid text: {s!r}")


def isjson(mimetype: str) -> bool:
    """
    Jinja test to check if a mimetype is json or json-like.
    """
    return mimetype == "application/json" or mimetype.endswith("+json")


def isb64image(mimetype: str) -> bool:
    """
    Jinja test to check if a mimetype is an base64-encoded image.
    """
    return bool(re.fullmatch(r"image/(png|jpeg|jpg)", mimetype))


class TemplateRenderer:
    def __init__(self):
        self.__env = Environment(
            loader=FileSystemLoader("templates"),
            auto_reload=False,
            autoescape=False,
            # autoescape=select_autoescape(),
        )
        # configure custom filters and tests
        self.__env.filters["get_source"] = get_source
        self._md_it = MarkdownIt()
        self.__env.filters["md2html"] = self._md_it.render
        self.__env.tests["isjson"] = isjson
        self.__env.tests["isb64image"] = isb64image

        self.__template = self.__env.get_template("export.html")

    def render(self, options: RenderOptions):
        return self.__template.render(
            filename=options.filename, date_=options.date_, notebook=options.notebook
        )
