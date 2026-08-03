import sys
from pathlib import Path


def _read_body(body: str | None, body_file: Path | None) -> str | None:
    """Resolve body text from --body or --body-file (supports '-' for stdin)."""
    if body is not None and body_file is not None:
        raise typer.BadParameter("Cannot use both --body and --body-file.")
    if body_file is not None:
        if str(body_file) == "-":
            return sys.stdin.read()
        return body_file.read_text(encoding="utf-8")
    return body

