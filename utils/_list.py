from typing import Any

def _list(value: list[Any], printer: ISortPrettyPrinter) -> str:
    return printer.pformat(sorted(value))


def _list(g: jit_utils.GraphContext, self):
    return self

