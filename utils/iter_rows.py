
def iter_rows(
    rows: cabc.Iterable[tuple[str, str]], col_count: int
) -> cabc.Iterator[tuple[str, ...]]:
    for row in rows:
        yield row + ("",) * (col_count - len(row))

