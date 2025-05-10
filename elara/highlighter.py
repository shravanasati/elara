from io import StringIO
import tokenize
import token

from elara.themes import Theme, extract_theme_data

BUILTINS = {"print", "len", "dict", "list", "int", "str", "range", "type"}


def map_token_type(tok_type: int, tok_string: str) -> str:
    if tok_type == token.STRING:
        return "string"
    elif tok_type == token.NUMBER:
        return "number"
    elif tok_type == token.COMMENT:
        return "comment"
    elif tok_type == token.NAME:
        if tok_string == "def":
            return "function_definition"
        elif tok_string == "class":
            return "class_definition"
        elif tok_string in {"return", "if", "else", "import"}:
            return "keyword"
        elif tok_string in BUILTINS:
            return "builtin"
        return "name"
    elif tok_type == token.OP:
        return "operator"
    return "default"


class SyntaxHighlighter:
    """
    Syntax highlighting for python, renders HTML.
    """

    def __init__(self, theme: Theme):
        self.theme = theme

    def highlight(self, source: str):
        """
        Injects span tags between the source with appropriate class names for styles.
        """
        output_tokens: list[str] = []
        last_end = (0, 0)
        tokens = tokenize.generate_tokens(StringIO(source).readline)

        for toknum, tokval, start, end, line in tokens:
            # Insert any whitespace between the previous token and the current one
            # print(f"{tokval=}")
            start_row, start_col = start
            end_row, end_col = end
            last_end_row, last_end_col = last_end

            if start_row == last_end_row:
                # Same line: insert the whitespace between tokens
                output_tokens.append(line[last_end_col:start_col])
            else:
                # Different lines: insert newlines and leading whitespace
                for i in range(last_end_row, start_row):
                    output_tokens.append("\n")
                output_tokens.append(line[:start_col])

            # Apply syntax highlighting
            tok_type = map_token_type(toknum, tokval)
            highlighted = f"<span class='token {tok_type}'>{tokval}</span>"
            output_tokens.append(highlighted)

            last_end = (end_row, end_col)

        return "".join(output_tokens)


if __name__ == "__main__":
    import json

    with open("./themes/vin-theme.json") as f:
        theme_json = json.load(f)
    sh = SyntaxHighlighter(extract_theme_data(theme_json))

    src = """
import token
print(4, "ss", token.HA)
"""
    print(sh.styles())
    print(sh.highlight(src))
