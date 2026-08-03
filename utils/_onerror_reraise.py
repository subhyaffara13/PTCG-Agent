from typing import Any

def _onerror_reraise(*_args: Any) -> None:
    raise  # noqa: PLE0704 - Bare exception used to reraise existing exception

