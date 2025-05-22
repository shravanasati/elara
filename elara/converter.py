import json
import logging

from jsonschema import ValidationError
from pygments.styles import get_all_styles

from elara.fileutils import FileLike, get_filename, open_file
from elara.notebook import Notebook
from elara.schema_validator import validate_notebook
from elara.template_renderer import RenderOptions, TemplateRenderer
from elara.themes import extract_theme_data


class Converter:
    """
    Builds the entire pipeline from reading the notebook, validating it,
    buildings models to represent it and finally render it according
    to the suitable style.
    """

    def __init__(self, theme_path: str, font: str, code_font: str):
        self.font = font
        self.code_font = code_font
        if theme_path in list(get_all_styles()):
            theme = theme_path
        else:
            try:
                with open_file(theme_path) as f:
                    theme_json = json.load(f)
                    theme = extract_theme_data(theme_json)
            except FileNotFoundError:
                print(f"Theme path {theme_path} not found!")
                exit(1)

        self.renderer = TemplateRenderer(theme)

    def convert(self, file: FileLike):
        try:
            with open_file(file) as f:
                nb_json = json.load(f)
            validate_notebook(nb_json)
            nb = Notebook(**nb_json)
            render_opts = RenderOptions(
                filename=get_filename(file),
                notebook=nb,
                font=self.font,
                code_font=self.code_font,
            )
            return self.renderer.render(render_opts)

        except FileNotFoundError:
            logging.error(f"File `{file}` not found.")
            # exit(1)

        except ValidationError as ve:
            logging.error(ve)
            # exit(1)

        except TypeError as te:
            logging.error("notebook construction failed, this should never happen")
            logging.error(te)


if __name__ == "__main__":
    c = Converter("nord", "gf:Oswald", "gf:Cascadia Mono")
    # c = Converter("./themes/latte.json")
    with open("test.html", "w") as f:
        output = c.convert("./samples/mine.ipynb")
        # output = c.convert("/home/shravan/Downloads/model_training.ipynb")
        if output is not None:
            f.write(output)
