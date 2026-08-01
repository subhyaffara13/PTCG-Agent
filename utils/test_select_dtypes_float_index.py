
def test_select_dtypes_float_index(temp_hdfstore):
    df = DataFrame(
        {
            "A": np.random.default_rng(2).random(20),
            "B": np.random.default_rng(2).random(20),
            "index": np.arange(20, dtype="f8"),
        }
    )
    temp_hdfstore.append("df_float", df)
    result = temp_hdfstore.select("df_float", "index<10.0 and columns=['A']")
    expected = df.reindex(index=list(df.index)[0:10], columns=["A"])
    tm.assert_frame_equal(expected, result)

