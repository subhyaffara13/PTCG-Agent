import sys
from pathlib import Path


def _output_io(name: Path) -> Iterator[IO[str]]:  # pragma: no cover
    """
    A context managing wrapper for pip-audit's `--output` flag. This allows us
    to avoid `argparse.FileType`'s "eager" file creation, which is generally
    the wrong/unexpected behavior when dealing with fallible processes.
    """
    if str(name) in {"stdout", "-"}:
        yield sys.stdout
    else:
        with name.open("w") as io:
            yield io

