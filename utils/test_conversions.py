
def test_conversions(data_missing):
    # astype to object series
    df = pd.DataFrame({"A": data_missing})
    result = df["A"].astype("object")
    expected = pd.Series(np.array([pd.NA, 1], dtype=object), name="A")
    tm.assert_series_equal(result, expected)

    # convert to object ndarray
    # we assert that we are exactly equal
    # including type conversions of scalars
    result = df["A"].astype("object").values
    expected = np.array([pd.NA, 1], dtype=object)
    tm.assert_numpy_array_equal(result, expected)

    for r, e in zip(result, expected, strict=True):
        if pd.isnull(r):
            assert pd.isnull(e)
        elif is_integer(r):
            assert r == e
            assert is_integer(e)
        else:
            assert r == e
            assert type(r) == type(e)


def test_conversions():
    # to_rgba_array("none") returns a (0, 4) array.
    assert_array_equal(mcolors.to_rgba_array("none"), np.zeros((0, 4)))
    assert_array_equal(mcolors.to_rgba_array([]), np.zeros((0, 4)))
    # a list of grayscale levels, not a single color.
    assert_array_equal(
        mcolors.to_rgba_array([".2", ".5", ".8"]),
        np.vstack([mcolors.to_rgba(c) for c in [".2", ".5", ".8"]]))
    # alpha is properly set.
    assert mcolors.to_rgba((1, 1, 1), .5) == (1, 1, 1, .5)
    assert mcolors.to_rgba(".1", .5) == (.1, .1, .1, .5)
    # builtin round differs between py2 and py3.
    assert mcolors.to_hex((.7, .7, .7)) == "#b2b2b2"
    # hex roundtrip.
    hex_color = "#1234abcd"
    assert mcolors.to_hex(mcolors.to_rgba(hex_color), keep_alpha=True) == \
        hex_color

