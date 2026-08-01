
def postgresql_adbc_types(postgresql_adbc_conn, types_data):
    import adbc_driver_manager as mgr

    conn = postgresql_adbc_conn

    try:
        conn.adbc_get_table_schema("types")
    except mgr.ProgrammingError:
        conn.rollback()
        new_data = [tuple(entry.values()) for entry in types_data]

        create_and_load_types_postgresql(conn, new_data)

    return conn

