
def sqlite_conn(sqlite_engine):
    with sqlite_engine.connect() as conn:
        yield conn

