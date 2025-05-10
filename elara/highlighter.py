from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name

from elara.themes import Theme, extract_theme_data


class SyntaxHighlighter:
    """
    Syntax highlighting for python, renders HTML.
    """

    def __init__(self, theme: Theme | str):
        if isinstance(theme, Theme):
            self.theme = theme
            self.formatter = HtmlFormatter(
                cssclass="highlight", style=self.theme.styles
            )
        elif isinstance(theme, str):
            try:
                self.theme = theme
                self.formatter = HtmlFormatter(
                    cssclass="highlight", style=get_style_by_name(theme)
                )

            except Exception:
                # theme not found
                print(f"Theme {theme} not found!")
                exit(1)

        else:
            print(f"Unknown {theme=} passed")
            exit(1)

        self.lexer = PythonLexer()

    def highlight(self, source: str):
        """
        Injects span tags between the source with appropriate class names for styles.
        """
        return highlight(source, self.lexer, self.formatter)


if __name__ == "__main__":
    import json

    with open("./themes/vin-theme.json") as f:
        theme_json = json.load(f)
    sh = SyntaxHighlighter(extract_theme_data(theme_json))

    src = """
import token
print(4, "ss", token.HA)
"""
    print(sh.highlight(src))
