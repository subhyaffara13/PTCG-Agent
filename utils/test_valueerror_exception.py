
def test_valueerror_exception(sqlite_engine):
    conn = sqlite_engine
    df = DataFrame({"col1": [1, 2], "col2": [3, 4]})
    with pytest.raises(ValueError, match="Empty table name specified"):
        df.to_sql(name="", con=conn, if_exists="replace", index=False)

