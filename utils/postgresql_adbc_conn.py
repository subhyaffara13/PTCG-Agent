
def postgresql_adbc_conn():
    pytest.importorskip("pyarrow")
    pytest.importorskip("adbc_driver_postgresql")
    from adbc_driver_postgresql import dbapi

    uri = "postgresql://postgres:postgres@localhost:5432/pandas"
    with dbapi.connect(uri) as conn:
        yield conn
        for view in get_all_views(conn):
            drop_view(view, conn)
        for tbl in get_all_tables(conn):
            drop_table(tbl, conn)
        conn.commit()

