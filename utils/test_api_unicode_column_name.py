
def test_api_unicode_column_name(conn, request):
    # GH 11431
    conn = request.getfixturevalue(conn)
    if sql.has_table("test_unicode", conn):
        with sql.SQLDatabase(conn, need_transaction=True) as pandasSQL:
            pandasSQL.drop_table("test_unicode")

    df = DataFrame([[1, 2], [3, 4]], columns=["\xe9", "b"])
    df.to_sql(name="test_unicode", con=conn, index=False)

