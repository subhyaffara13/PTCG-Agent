
def test_query_by_text_obj(conn, request):
    # WIP : GH10846
    conn_name = conn
    conn = request.getfixturevalue(conn)
    from sqlalchemy import text

    if "postgres" in conn_name:
        name_text = text('select * from iris where "Name"=:name')
    else:
        name_text = text("select * from iris where name=:name")
    iris_df = sql.read_sql(name_text, conn, params={"name": "Iris-versicolor"})
    all_names = set(iris_df["Name"])
    assert all_names == {"Iris-versicolor"}

