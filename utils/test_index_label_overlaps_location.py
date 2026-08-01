
def test_index_label_overlaps_location():
    # checking we don't have any label/location confusion in the
    # wake of GH5375
    df = DataFrame(list("ABCDE"), index=[2, 0, 2, 1, 1])
    g = df.groupby(list("ababb"))
    actual = g.filter(lambda x: len(x) > 2)
    expected = df.iloc[[1, 3, 4]]
    tm.assert_frame_equal(actual, expected)

    ser = df[0]
    g = ser.groupby(list("ababb"))
    actual = g.filter(lambda x: len(x) > 2)
    expected = ser.take([1, 3, 4])
    tm.assert_series_equal(actual, expected)

    #  and again, with a generic Index of floats
    df.index = df.index.astype(float)
    g = df.groupby(list("ababb"))
    actual = g.filter(lambda x: len(x) > 2)
    expected = df.iloc[[1, 3, 4]]
    tm.assert_frame_equal(actual, expected)

    ser = df[0]
    g = ser.groupby(list("ababb"))
    actual = g.filter(lambda x: len(x) > 2)
    expected = ser.take([1, 3, 4])
    tm.assert_series_equal(actual, expected)

