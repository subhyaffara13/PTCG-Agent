
def test_broadcast(size, mask, item, box):
    # GH#8801, GH#4195
    selection = np.resize(mask, size)

    data = np.arange(size, dtype=float)

    # Construct the expected series by taking the source
    # data or item based on the selection
    expected = Series(
        [item if use_item else data[i] for i, use_item in enumerate(selection)]
    )

    s = Series(data)

    s[selection] = item
    tm.assert_series_equal(s, expected)

    s = Series(data)
    result = s.where(~selection, box([item]))
    tm.assert_series_equal(result, expected)

    s = Series(data)
    result = s.mask(selection, box([item]))
    tm.assert_series_equal(result, expected)

