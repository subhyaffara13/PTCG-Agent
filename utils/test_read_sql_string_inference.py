
def test_read_sql_string_inference(sqlite_engine):
    conn = sqlite_engine
    # GH#54430
    table = "test"
    df = DataFrame({"a": ["x", "y"]})
    df.to_sql(table, con=conn, index=False, if_exists="replace")

    with pd.option_context("future.infer_string", True):
        result = read_sql_table(table, conn)

    dtype = pd.StringDtype(na_value=np.nan)
    expected = DataFrame(
        {"a": ["x", "y"]}, dtype=dtype, columns=Index(["a"], dtype=dtype)
    )

    tm.assert_frame_equal(result, expected)

