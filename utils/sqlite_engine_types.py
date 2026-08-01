
def sqlite_engine_types(sqlite_engine, types_data):
    create_and_load_types(sqlite_engine, types_data, "sqlite")
    return sqlite_engine

