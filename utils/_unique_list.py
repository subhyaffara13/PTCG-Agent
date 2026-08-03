from typing import Any

def _unique_list(value: list[Any], printer: ISortPrettyPrinter) -> str:
    return printer.pformat(sorted(set(value)))

