
def test_arithmetic_multiindex_column_align():
    # GH#60498
    df1 = DataFrame(
        data=100,
        columns=MultiIndex.from_product(
            [["1A", "1B"], ["2A", "2B"]], names=["Lev1", "Lev2"]
        ),
        index=["C1", "C2"],
    )
    df2 = DataFrame(
        data=np.array([[0.1, 0.25], [0.2, 0.45]]),
        columns=MultiIndex.from_product([["1A", "1B"]], names=["Lev1"]),
        index=["C1", "C2"],
    )
    expected = DataFrame(
        data=np.array([[10.0, 10.0, 25.0, 25.0], [20.0, 20.0, 45.0, 45.0]]),
        columns=MultiIndex.from_product(
            [["1A", "1B"], ["2A", "2B"]], names=["Lev1", "Lev2"]
        ),
        index=["C1", "C2"],
    )
    result = df1 * df2
    tm.assert_frame_equal(result, expected)

