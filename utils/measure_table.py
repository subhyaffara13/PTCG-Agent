
def measure_table(rows: cabc.Iterable[tuple[str, str]]) -> tuple[int, ...]:
    widths: dict[int, int] = {}

    for row in rows:
        for idx, col in enumerate(row):
            widths[idx] = max(widths.get(idx, 0), term_len(col))

    return tuple(y for x, y in sorted(widths.items()))

