
def sqlite_adbc_types(sqlite_adbc_conn, types_data):
    import adbc_driver_manager as mgr

    conn = sqlite_adbc_conn
    try:
        conn.adbc_get_table_schema("types")
    except mgr.ProgrammingError:
        conn.rollback()
        new_data = []
        for entry in types_data:
            entry["BoolCol"] = int(entry["BoolCol"])
            if entry["BoolColWithNull"] is not None:
                entry["BoolColWithNull"] = int(entry["BoolColWithNull"])
            new_data.append(tuple(entry.values()))

        create_and_load_types_sqlite3(conn, new_data)
        conn.commit()

    return conn

