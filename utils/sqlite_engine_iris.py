
def sqlite_engine_iris(sqlite_engine, iris_path):
    create_and_load_iris(sqlite_engine, iris_path)
    create_and_load_iris_view(sqlite_engine)
    return sqlite_engine

