
def _raise_on_forbidden_query(query: str) -> None:
    if len(query) == 0:
        raise ValueError("SQL query cannot be empty.")

    # DuckDB CLI meta-commands are dot-prefixed words (e.g. `.shell`, `.output`).
    # Let's forbid them for now but allow SQL expressions like `.5` that can legitimately start a line.
    for line in query.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(".") and stripped[1:2].isalpha():
            raise ValueError("DuckDB CLI meta-commands are not allowed in SQL queries.")

