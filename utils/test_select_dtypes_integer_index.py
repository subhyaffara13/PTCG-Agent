
def test_select_dtypes_integer_index(temp_hdfstore):
    df = DataFrame(
        {
            "A": np.random.default_rng(2).random(20),
            "B": np.random.default_rng(2).random(20),
        }
    )
    temp_hdfstore.append("df_int", df)
    result = temp_hdfstore.select("df_int", "index<10 and columns=['A']")
    expected = df.reindex(index=list(df.index)[0:10], columns=["A"])
    tm.assert_frame_equal(expected, result)

