from contextlib import contextmanager
from typing import Generator, IO
import os
from pathlib import Path

FileLike = str | Path | os.PathLike | IO


@contextmanager
def open_file(
    file: FileLike, mode="r", encoding="utf-8"
) -> Generator[IO, None, None]:
    if hasattr(file, "read") or hasattr(file, "write"):
        # already a file-like object
        yield file
    else:
        # it's a path
        with open(file, mode, encoding=encoding) as f:
            yield f


def get_filename(file: FileLike) -> str:
    if hasattr(file, "read") or hasattr(file, "write"):
        return "stream"
    else:
        # it's a path
        return Path(file).stem
