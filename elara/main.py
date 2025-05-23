from pathlib import Path
from typing import Annotated

import typer
from pygments.styles import get_all_styles
from rich import print
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

from elara.converter import Converter

SHORT_HELP_TEXT = (
    """elara is a CLI tool to convert Jupyter notebooks into *pretty* HTML documents."""
)

HELP_TEXT = f"""
{SHORT_HELP_TEXT}

elara is very much customizable while providing sane defaults.

For more information, visit https://github.com/shravanasati/elara
"""

app = typer.Typer(
    name="elara", help=HELP_TEXT, short_help=SHORT_HELP_TEXT, no_args_is_help=True
)


@app.command()
def list_themes():
    """
    Lists all built-in themes.
    """
    print(list(get_all_styles()))


def get_output_filename(file: str):
    """
    Returns a non-existent HTML output file name.
    """
    filename_wo_ext = "".join(file.split(".ipynb")[:-1])
    output_filename = filename_wo_ext + ".html"
    output_path = Path(output_filename)
    count = 1
    while output_path.exists():
        output_filename = f"{filename_wo_ext}({count}).html"
        count += 1
        output_path = Path(output_filename)

    return output_filename


def handle_file_conversion(input_file: str, output_filepath: str, converter: Converter):
    """
    Actually converts the given notebook file using the passed converter object.
    """
    output = converter.convert(input_file)
    if output is not None:
        with open(output_filepath, "w") as f:
            f.write(output)


@app.command()
def convert(
    files: list[str],
    theme: Annotated[str, typer.Option(help="The theme for code blocks.")] = "vs",
    font: Annotated[
        str, typer.Option(help="Font for overall document.")
    ] = "sans-serif",
    code_font: Annotated[
        str, typer.Option(help="Font for code and output.")
    ] = "monospace",
    silent: Annotated[
        bool, typer.Option(help="Silent output, print only the exported file names.")
    ] = False,
):
    """
    Converts multiple jupyter notebooks into HTML documents. Any options passed, will be applied to all
    the jupyter notebooks.

    Font options can be prefixed with `gf:` to use Google Fonts directly.
    """
    spinner = SpinnerColumn("moon")
    text_col = TextColumn("[yellow]Converting[/]")
    bar_col = BarColumn(None)
    progress = Progress(spinner, text_col, bar_col)
    converter = Converter(theme, font, code_font)
    if silent:
        # only prints the output filenames
        # used by the vscode extension
        for file in files:
            output_filename = get_output_filename(file)
            handle_file_conversion(file, output_filename, converter)
            print(output_filename)
    else:
        # default look for CLI users
        with progress:
            for file in progress.track(files):
                output_filename = get_output_filename(file)
                progress.print(
                    f"Exporting [cyan]{file}[/] to [green bold]{output_filename}[/]..."
                )
                handle_file_conversion(file, output_filename, converter)


if __name__ == "__main__":
    app()
