
def _set(value: set[Any], printer: ISortPrettyPrinter) -> str:
    return "{" + printer.pformat(tuple(sorted(value)))[1:-1] + "}"

