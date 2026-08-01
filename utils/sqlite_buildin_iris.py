
def sqlite_buildin_iris(sqlite_buildin, iris_path):
    create_and_load_iris_sqlite3(sqlite_buildin, iris_path)
    create_and_load_iris_view(sqlite_buildin)
    return sqlite_buildin

