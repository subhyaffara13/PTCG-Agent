
def test_pad_stable_sorting(fill_method):
    # GH 21207
    x = [0] * 20
    y = [np.nan] * 10 + [1] * 10

    if fill_method == "bfill":
        y = y[::-1]

    df = DataFrame({"x": x, "y": y})
    expected = df.drop("x", axis=1)

    result = getattr(df.groupby("x"), fill_method)()

    tm.assert_frame_equal(result, expected)

