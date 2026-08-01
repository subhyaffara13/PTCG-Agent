
def sqlite_adbc_conn(temp_file):
    pytest.importorskip("pyarrow")
    pytest.importorskip("adbc_driver_sqlite")
    from adbc_driver_sqlite import dbapi

    uri = f"file:{temp_file}"
    with dbapi.connect(uri) as conn:
        yield conn
        for view in get_all_views(conn):
            drop_view(view, conn)
        for tbl in get_all_tables(conn):
            drop_table(tbl, conn)
        conn.commit()

