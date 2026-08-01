
def sqlite_conn_types(sqlite_engine_types):
    with sqlite_engine_types.connect() as conn:
        yield conn

