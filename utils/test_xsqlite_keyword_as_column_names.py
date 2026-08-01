
def test_xsqlite_keyword_as_column_names(sqlite_buildin):
    df = DataFrame({"From": np.ones(5)})
    assert sql.to_sql(df, con=sqlite_buildin, name="testkeywords", index=False) == 5

