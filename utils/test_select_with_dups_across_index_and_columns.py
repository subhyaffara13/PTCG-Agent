
def test_select_with_dups_across_index_and_columns(temp_hdfstore):
    df = concat(
        [
            DataFrame(
                np.random.default_rng(2).standard_normal((10, 4)),
                columns=["A", "A", "B", "B"],
            ),
            DataFrame(
                np.random.default_rng(2).integers(0, 10, size=20).reshape(10, 2),
                columns=["A", "C"],
            ),
        ],
        axis=1,
    )
    df.index = date_range("20130101 9:30", periods=10, freq="min", unit="ns")
    temp_hdfstore.append("df", df)
    temp_hdfstore.append("df", df)

    expected = df.loc[:, ["B", "A"]]
    expected = concat([expected, expected])
    result = temp_hdfstore.select("df", columns=["B", "A"])
    tm.assert_frame_equal(result, expected, by_blocks=True)

