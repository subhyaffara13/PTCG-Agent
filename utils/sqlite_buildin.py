
def sqlite_buildin():
    with contextlib.closing(sqlite3.connect(":memory:")) as closing_conn:
        with closing_conn as conn:
            yield conn

