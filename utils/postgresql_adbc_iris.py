
def postgresql_adbc_iris(postgresql_adbc_conn, iris_path):
    import adbc_driver_manager as mgr

    conn = postgresql_adbc_conn

    try:
        conn.adbc_get_table_schema("iris")
    except mgr.ProgrammingError:
        conn.rollback()
        create_and_load_iris_postgresql(conn, iris_path)
    try:
        conn.adbc_get_table_schema("iris_view")
    except mgr.ProgrammingError:  # note arrow-adbc issue 1022
        conn.rollback()
        create_and_load_iris_view(conn)
    return conn

