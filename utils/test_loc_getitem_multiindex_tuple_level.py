
def test_loc_getitem_multiindex_tuple_level():
    # GH#27591
    lev1 = ["a", "b", "c"]
    lev2 = [(0, 1), (1, 0)]
    lev3 = [0, 1]
    cols = MultiIndex.from_product([lev1, lev2, lev3], names=["x", "y", "z"])
    df = DataFrame(6, index=range(5), columns=cols)

    # the lev2[0] here should be treated as a single label, not as a sequence
    #  of labels
    result = df.loc[:, (lev1[0], lev2[0], lev3[0])]

    # TODO: i think this actually should drop levels
    expected = df.iloc[:, :1]
    tm.assert_frame_equal(result, expected)

    alt = df.xs((lev1[0], lev2[0], lev3[0]), level=[0, 1, 2], axis=1)
    tm.assert_frame_equal(alt, expected)

    # same thing on a Series
    ser = df.iloc[0]
    expected2 = ser.iloc[:1]

    alt2 = ser.xs((lev1[0], lev2[0], lev3[0]), level=[0, 1, 2], axis=0)
    tm.assert_series_equal(alt2, expected2)

    result2 = ser.loc[lev1[0], lev2[0], lev3[0]]
    assert result2 == 6

