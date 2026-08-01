
def test_start_stop_table(temp_hdfstore):
    # table
    df = DataFrame(
        {
            "A": np.random.default_rng(2).random(20),
            "B": np.random.default_rng(2).random(20),
        }
    )
    temp_hdfstore.append("df", df)

    result = temp_hdfstore.select("df", "columns=['A']", start=0, stop=5)
    expected = df.loc[0:4, ["A"]]
    tm.assert_frame_equal(result, expected)

    # out of range
    result = temp_hdfstore.select("df", "columns=['A']", start=30, stop=40)
    assert len(result) == 0
    expected = df.loc[30:40, ["A"]]
    tm.assert_frame_equal(result, expected)

