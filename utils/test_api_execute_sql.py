
def test_api_execute_sql(conn, request):
    # drop_sql = "DROP TABLE IF EXISTS test"  # should already be done
    conn = request.getfixturevalue(conn)
    with sql.pandasSQL_builder(conn) as pandas_sql:
        iris_results = pandas_sql.execute("SELECT * FROM iris")
        row = iris_results.fetchone()
        iris_results.close()
    assert list(row) == [5.1, 3.5, 1.4, 0.2, "Iris-setosa"]

