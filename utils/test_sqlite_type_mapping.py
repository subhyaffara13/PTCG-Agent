
def test_sqlite_type_mapping(sqlite_buildin):
    # Test Timestamp objects (no datetime64 because of timezone) (GH9085)
    conn = sqlite_buildin
    df = DataFrame(
        {"time": to_datetime(["2014-12-12 01:54", "2014-12-11 02:54"], utc=True)}
    )
    db = sql.SQLiteDatabase(conn)
    table = sql.SQLiteTable("test_type", db, frame=df)
    schema = table.sql_schema()
    for col in schema.split("\n"):
        if col.split()[0].strip('"') == "time":
            assert col.split()[1] == "TIMESTAMP"

