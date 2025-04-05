from dataclasses import dataclass
from typing import Any

frozenSlottedKwOnlyDataclass = dataclass(frozen=True, slots=True, kw_only=True)

CellID = str
Metadata = dict[str, Any]
Source = str | list[str]
MimeBundle = dict[str, str]


@frozenSlottedKwOnlyDataclass
class ExecuteResult:
    output_type: str = "execute_result"
    data: MimeBundle
    metadata: Metadata
    execution_count: int | None


@frozenSlottedKwOnlyDataclass
class DisplayData:
    output_type: str = "display_data"
    data: MimeBundle
    metadata: Metadata


@frozenSlottedKwOnlyDataclass
class Stream:
    output_type: str = "stream"
    name: str
    text: Source


@frozenSlottedKwOnlyDataclass
class Error:
    output_type: str = "error"
    ename: str
    evalue: str
    traceback: list[str]


Output = ExecuteResult | DisplayData | Stream | Error


@frozenSlottedKwOnlyDataclass
class MarkdownCell:
    id: CellID
    cell_type: str = "markdown"
    metadata: Metadata
    source: Source


@frozenSlottedKwOnlyDataclass
class CodeCell:
    id: CellID
    cell_type: str = "code"
    metadata: Metadata
    source: Source
    outputs: list[Output]
    execution_count: int | None


Cell = MarkdownCell | CodeCell


@frozenSlottedKwOnlyDataclass
class Notebook:
    metadata: Metadata
    nbformat_minor: int
    nbformat: int
    cells: list[Cell]


if __name__ == "__main__":
    import json

    with open("./sample.ipynb") as f:
        nb = Notebook(**json.load(f))
        print(nb)
