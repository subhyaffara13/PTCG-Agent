
def test_query_by_select_obj(conn, request):
    conn = request.getfixturevalue(conn)
    # WIP : GH10846
    from sqlalchemy import (
        bindparam,
        select,
    )

    iris = iris_table_metadata()
    name_select = select(iris).where(iris.c.Name == bindparam("name"))
    iris_df = sql.read_sql(name_select, conn, params={"name": "Iris-setosa"})
    all_names = set(iris_df["Name"])
    assert all_names == {"Iris-setosa"}

