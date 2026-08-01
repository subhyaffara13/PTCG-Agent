
def sqlite_builtin_detect_types():
    with contextlib.closing(
        sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
    ) as closing_conn:
        with closing_conn as conn:
            yield conn

