
def sqlite_buildin_types(sqlite_buildin, types_data):
    types_data = [tuple(entry.values()) for entry in types_data]
    create_and_load_types_sqlite3(sqlite_buildin, types_data)
    return sqlite_buildin

