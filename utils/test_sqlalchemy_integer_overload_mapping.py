
def test_sqlalchemy_integer_overload_mapping(conn, request, integer):
    conn = request.getfixturevalue(conn)
    # GH35076 Map pandas integer to optimal SQLAlchemy integer type
    df = DataFrame([0, 1], columns=["a"], dtype=integer)
    with sql.SQLDatabase(conn) as db:
        with pytest.raises(
            ValueError, match="Unsigned 64 bit integer datatype is not supported"
        ):
            sql.SQLTable("test_type", db, frame=df)

