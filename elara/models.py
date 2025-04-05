from pydantic import BaseModel, Field
from typing import Union, Literal, List, Optional, Annotated, Any, Dict


CellID = str
Metadata = Dict[str, Any]
Source = Union[str, List[str]]
MimeBundle = Dict[str, str]


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

    def get_source(self) -> str:
        if isinstance(self.text, str):
            return self.text
        elif isinstance(self.text, list):
            return "".join(self.text)
        raise ValueError(f"Invalid text: {self.text!r}")


class Error(BaseModel):
    output_type: Literal["error"] = "error"
    ename: str
    evalue: str
    traceback: List[str]


Output = Annotated[
    Union[ExecuteResult, DisplayData, Stream, Error], Field(discriminator="output_type")
]


class CellBase(BaseModel):
    id: Optional[CellID] = None
    metadata: Metadata
    source: Source

    def get_source(self) -> str:
        if isinstance(self.source, str):
            return self.source
        elif isinstance(self.source, list):
            return "".join(self.source)
        raise ValueError(f"Invalid source: {self.source!r}")


class MarkdownCell(CellBase):
    cell_type: Literal["markdown"] = "markdown"


class CodeCell(CellBase):
    cell_type: Literal["code"] = "code"
    outputs: List[Output]
    execution_count: Optional[int]


Cell = Annotated[Union[MarkdownCell, CodeCell], Field(discriminator="cell_type")]


class Notebook(BaseModel):
    metadata: Metadata
    nbformat_minor: int
    nbformat: int
    cells: List[Cell]


if __name__ == "__main__":
    import json

    with open("./sample.ipynb") as f:
        nb = Notebook(**json.load(f))
        print(nb)
