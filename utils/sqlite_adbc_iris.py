
def sqlite_adbc_iris(sqlite_adbc_conn, iris_path):
    import adbc_driver_manager as mgr

    conn = sqlite_adbc_conn
    try:
        conn.adbc_get_table_schema("iris")
    except mgr.ProgrammingError:
        conn.rollback()
        create_and_load_iris_sqlite3(conn, iris_path)
    try:
        conn.adbc_get_table_schema("iris_view")
    except mgr.ProgrammingError:
        conn.rollback()
        create_and_load_iris_view(conn)
    return conn

