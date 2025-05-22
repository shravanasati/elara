import json
import re
from dataclasses import asdict, dataclass
from datetime import date
from functools import partial
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

from ansi2html import Ansi2HTMLConverter
from jinja2 import Environment, FileSystemLoader  # , select_autoescape
from markdown_it import MarkdownIt
from pygments.styles import get_style_by_name

from elara.highlighter import SyntaxHighlighter
from elara.notebook import Notebook
from elara.themes import Theme


@dataclass(frozen=True, slots=True)
class RenderOptions:
    filename: str
    notebook: Notebook
    font: str
    code_font: str
    date_: date = date.today()

    def as_dict(self):
        return asdict(self)


def get_source(s: str | list[str] | dict[Any, Any]) -> str:
    """
    Jinja filter to render model `Source`.
    """
    if isinstance(s, str):
        return s
    elif isinstance(s, list):
        return "".join(s)
    elif isinstance(s, dict):
        return json.dumps(s)
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


def is_google_font(font_name: str) -> bool:
    """
    Jinja test to check if the font name is a google font.
    """
    return font_name.startswith("gf:")


def format_google_font(font_name: str) -> str:
    """
    Jinja filter to format a font name for a URL. Removes 'gf:' prefix and quotes it.
    """
    if not is_google_font(font_name):
        raise ValueError(
            f"non google-font {font_name=} passed to format_google_font filter"
        )

    return quote_plus(font_name[3:])


class TemplateRenderer:
    def __init__(self, theme: Theme | str):
        templates_path = Path(__file__).parent / "templates"
        self.__env = Environment(
            loader=FileSystemLoader(str(templates_path)),
            auto_reload=False,
            autoescape=False,
            # autoescape=select_autoescape(),
        )
        # configure custom filters and tests
        self.__env.filters["get_source"] = get_source

        self._md_it = MarkdownIt()
        self.__env.filters["md2html"] = self._md_it.render

        self._ansi2html = Ansi2HTMLConverter(dark_bg=False)
        self.__env.filters["ansi2html"] = partial(self._ansi2html.convert, full=False)

        self.theme = theme
        self._syntax_highlighter = SyntaxHighlighter(theme)
        self.__env.filters["highlight"] = self._syntax_highlighter.highlight
        if isinstance(self.theme, Theme):
            self.bg_color = self.theme.raw_colors.get("editor.background")
        elif isinstance(self.theme, str):
            self.bg_color = get_style_by_name(self.theme).background_color

        self._css_styles = self._syntax_highlighter.formatter.get_style_defs(
            ".highlight"
        )

        self.__env.tests["isjson"] = isjson
        self.__env.tests["isb64image"] = isb64image

        self.__env.tests["is_google_font"] = is_google_font
        self.__env.filters["format_google_font"] = format_google_font

        self.__template = self.__env.get_template("export.html")

    def render(self, options: RenderOptions):
        # todo make date optional
        # todo if font and code_font are different, fetch them in a single request
        # add family query param in the URL
        return self.__template.render(
            filename=options.filename,
            date_=options.date_,
            notebook=options.notebook,
            bg_color=self.bg_color,
            styles=self._css_styles,
            font=options.font,
            code_font=options.code_font,
        )
