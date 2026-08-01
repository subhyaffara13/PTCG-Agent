
def _format_row(values: Sequence[int], width: int = 3) -> str:
    return " ".join(str(v).rjust(width) for v in values)

