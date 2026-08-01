
def test_read_iris_query_expression_with_parameter(conn, request):
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(
                reason="'chunksize' not implemented for ADBC drivers",
                strict=True,
            )
        )
    conn = request.getfixturevalue(conn)
    from sqlalchemy import (
        MetaData,
        Table,
        create_engine,
        select,
    )

    metadata = MetaData()
    autoload_con = create_engine(conn) if isinstance(conn, str) else conn
    iris = Table("iris", metadata, autoload_with=autoload_con)
    iris_frame = read_sql_query(
        select(iris), conn, params={"name": "Iris-setosa", "length": 5.1}
    )
    check_iris_frame(iris_frame)
    if isinstance(conn, str):
        autoload_con.dispose()

