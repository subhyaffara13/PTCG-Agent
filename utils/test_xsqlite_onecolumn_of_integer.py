
def test_xsqlite_onecolumn_of_integer(sqlite_buildin):
    # GH 3628
    # a column_of_integers dataframe should transfer well to sql

    mono_df = DataFrame([1, 2], columns=["c0"])
    assert sql.to_sql(mono_df, con=sqlite_buildin, name="mono_df", index=False) == 2
    # computing the sum via sql
    con_x = sqlite_buildin
    the_sum = sum(my_c0[0] for my_c0 in con_x.execute("select * from mono_df"))
    # it should not fail, and gives 3 ( Issue #3628 )
    assert the_sum == 3

    result = sql.read_sql("select * from mono_df", con_x)
    tm.assert_frame_equal(result, mono_df)

