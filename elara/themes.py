from typing import Any, Dict, Optional

from pydantic import BaseModel
from pygments.style import Style
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Token,
)


class ThemeColor(BaseModel):
    """Represents a generic color value from a VS Code theme."""

    foreground: Optional[str] = None  # Text color (e.g., "#RRGGBB")
    background: Optional[str] = None  # Background color
    font_style: Optional[str] = None  # "italic", "bold", "underline", or combinations


class PythonCodeColors(BaseModel):
    """Represents colors for Python source code elements."""

    comment: Optional[str] = None
    keyword: Optional[str] = None
    string: Optional[str] = None
    number: Optional[str] = None
    function_definition: Optional[str] = None
    function_call: Optional[str] = None
    class_definition: Optional[str] = None
    variable: Optional[str] = None
    operator: Optional[str] = None
    punctuation: Optional[str] = None
    builtin: Optional[str] = None  # Built-in functions, types, constants


class HTMLColors(BaseModel):
    """Represents colors for the overall HTML structure."""

    body_background: Optional[str] = None
    body_foreground: Optional[str] = None
    heading: Optional[str] = None  # Default color for headings
    link: Optional[str] = None
    link_hover: Optional[str] = None
    code_background: Optional[str] = None  # Background for code blocks in HTML
    code_foreground: Optional[str] = None  # Foreground for code blocks in HTML
    blockquote_background: Optional[str] = None
    blockquote_foreground: Optional[str] = None


class Theme(BaseModel):
    """Represents relevant color data extracted from a VS Code theme."""

    name: str
    is_dark: Optional[bool] = None
    python_code: PythonCodeColors = PythonCodeColors()
    html: HTMLColors = HTMLColors()
    raw_colors: Optional[Dict[str, str]] = (
        None  # Optionally store the raw 'colors' section
    )
    raw_token_colors: Optional[list[Dict]] = (
        None  # Optionally store the raw 'tokenColors' section
    )

    @property
    def styles(self):
        """
        Returns a custom styles object that can be passed to the pygments formatter.
        """
        colors = self.python_code
        default_color = self.raw_colors.get("editor.foreground", "#ffffff")

        def color_or_default(c: str | None):
            if c is None:
                return default_color

            return c

        class CustomStyle(Style):
            styles = {
                Token: "",
                Comment: color_or_default(colors.comment),
                Keyword: color_or_default(colors.keyword),
                String: color_or_default(colors.keyword),
                Number: color_or_default(colors.number),
                Name: default_color,
                Name.Function: color_or_default(colors.function_definition),
                Name.Class: color_or_default(colors.class_definition),
                Name.Variable: color_or_default(colors.variable),
                Operator: color_or_default(colors.operator),
                Punctuation: color_or_default(colors.punctuation),
            }

        return CustomStyle


def extract_theme_data(theme_json: dict[str, Any]) -> Theme:
    theme_data = Theme(name=theme_json.get("name", "Unnamed Theme"))
    theme_data.is_dark = theme_json.get("type") == "dark"
    theme_data.raw_colors = theme_json.get("colors")
    theme_data.raw_token_colors = theme_json.get("tokenColors")

    default_foreground = (
        theme_data.raw_colors.get("editor.foreground")
        if theme_data.raw_colors
        else "#FFF"
    )

    if theme_data.raw_colors:
        theme_data.html.body_background = theme_data.raw_colors.get("editor.background")
        theme_data.html.body_foreground = theme_data.raw_colors.get("editor.foreground")
        theme_data.html.code_background = theme_data.raw_colors.get("editor.background")
        theme_data.html.code_foreground = theme_data.raw_colors.get("editor.foreground")
        theme_data.html.link = theme_data.raw_colors.get("textLink.foreground")
        theme_data.html.link_hover = theme_data.raw_colors.get(
            "textLink.activeForeground"
        )

    if theme_data.raw_token_colors:
        for rule in theme_data.raw_token_colors:
            scope = rule.get("scope")
            settings = rule.get("settings", {})
            foreground = settings.get("foreground")

            if isinstance(scope, str):
                if "comment" in scope:
                    theme_data.python_code.comment = foreground
                elif "keyword" in scope:
                    theme_data.python_code.keyword = foreground
                elif "string" in scope:
                    theme_data.python_code.string = foreground
                elif "constant.numeric" in scope:
                    theme_data.python_code.number = foreground
                elif "entity.name.function" in scope:
                    theme_data.python_code.function_definition = (
                        foreground  # Or differentiate call
                    )
                elif "variable" in scope:
                    theme_data.python_code.variable = foreground
                elif "keyword.operator" in scope:
                    theme_data.python_code.operator = foreground
                elif "punctuation" in scope:
                    theme_data.python_code.punctuation = foreground
                elif "support.function.builtin" in scope:
                    theme_data.python_code.builtin = foreground
                elif "entity.name.class" in scope:
                    theme_data.python_code.class_definition = foreground
                # Add more mappings as needed
            elif isinstance(scope, list):
                for s in scope:
                    if "comment" in s:
                        theme_data.python_code.comment = foreground
                        break
                    elif "keyword" in s:
                        theme_data.python_code.keyword = foreground
                        break
                    elif "string" in s:
                        theme_data.python_code.string = foreground
                        break
                    elif "constant.numeric" in s:
                        theme_data.python_code.number = foreground
                        break
                    elif "entity.name.function" in s:
                        theme_data.python_code.function_definition = foreground
                        break
                    elif "variable" in s:
                        theme_data.python_code.variable = foreground
                        break
                    elif "keyword.operator" in s:
                        theme_data.python_code.operator = foreground
                        break
                    elif "punctuation" in s:
                        theme_data.python_code.punctuation = foreground
                        break
                    elif "support.function.builtin" in s:
                        theme_data.python_code.builtin = foreground
                        break
                    elif "entity.name.class" in s:
                        theme_data.python_code.class_definition = foreground
                        break

    # Set default foreground for any None values in python_code
    for field in theme_data.python_code.__class__.model_fields:
        field_value = getattr(theme_data.python_code, field)
        if field_value is None:
            setattr(theme_data.python_code, field, default_foreground)

    return theme_data


if __name__ == "__main__":
    import json

    with open("./themes/vin-theme.json") as f:
        theme_json = json.load(f)

    print(extract_theme_data(theme_json))
