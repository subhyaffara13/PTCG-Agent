
def test_con_unknown_dbapi2_class_does_not_error_without_sql_alchemy_installed():
    class MockSqliteConnection:
        def __init__(self, *args, **kwargs) -> None:
            self.conn = sqlite3.Connection(*args, **kwargs)

        def __getattr__(self, name):
            return getattr(self.conn, name)

        def close(self):
            self.conn.close()

    with contextlib.closing(MockSqliteConnection(":memory:")) as conn:
        with tm.assert_produces_warning(UserWarning, match="only supports SQLAlchemy"):
            sql.read_sql("SELECT 1", conn)

