
def sqlite_conn_iris(sqlite_engine_iris):
    with sqlite_engine_iris.connect() as conn:
        yield conn

