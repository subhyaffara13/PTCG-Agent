
def test_sqlalchemy_integer_mapping(conn, request, integer, expected):
    # GH35076 Map pandas integer to optimal SQLAlchemy integer type
    conn = request.getfixturevalue(conn)
    df = DataFrame([0, 1], columns=["a"], dtype=integer)
    with sql.SQLDatabase(conn) as db:
        table = sql.SQLTable("test_type", db, frame=df)

        result = str(table.table.c.a.type)
    assert result == expected

