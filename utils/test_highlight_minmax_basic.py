
def test_highlight_minmax_basic(df, f):
    expected = {
        (0, 1): [("background-color", "red")],
        # ignores NaN row,
        (2, 0): [("background-color", "red")],
    }
    if f == "highlight_min":
        df = -df
    result = getattr(df.style, f)(axis=1, color="red")._compute().ctx
    assert result == expected

