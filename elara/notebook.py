from typing import Annotated, Any, Literal, Optional, Union

from pydantic import BaseModel, Field

CellID = str
Metadata = dict[str, Any]
Source = Union[str, list[str]]
MimeBundle = dict[str, str | list[str] | dict[str, Any]]


class ExecuteResult(BaseModel):
    output_type: Literal["execute_result"] = "execute_result"
    data: MimeBundle
    metadata: Metadata
    execution_count: Optional[int]


class DisplayData(BaseModel):
    output_type: Literal["display_data"] = "display_data"
    data: MimeBundle
    metadata: Metadata


class Stream(BaseModel):
    output_type: Literal["stream"] = "stream"
    name: str
    text: Source


class Error(BaseModel):
    output_type: Literal["error"] = "error"
    ename: str
    evalue: str
    traceback: list[str]


Output = Annotated[
    Union[ExecuteResult, DisplayData, Stream, Error], Field(discriminator="output_type")
]


class CellBase(BaseModel):
    id: Optional[CellID] = None
    metadata: Metadata
    source: Source


class MarkdownCell(CellBase):
    cell_type: Literal["markdown"] = "markdown"


class CodeCell(CellBase):
    cell_type: Literal["code"] = "code"
    outputs: list[Output]
    execution_count: Optional[int]


Cell = Annotated[Union[MarkdownCell, CodeCell], Field(discriminator="cell_type")]


class Notebook(BaseModel):
    metadata: Metadata
    nbformat_minor: int
    nbformat: int
    cells: list[Cell]


if __name__ == "__main__":
    import json

    with open("./sample.ipynb") as f:
        nb = Notebook(**json.load(f))
        print(nb)
