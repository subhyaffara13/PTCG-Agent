from typing import Any

def _unique_tuple(value: tuple[Any, ...], printer: ISortPrettyPrinter) -> str:
    return printer.pformat(tuple(sorted(set(value))))

