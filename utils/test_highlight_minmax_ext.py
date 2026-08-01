
def test_highlight_minmax_ext(df, f, kwargs):
    expected = {(2, 0): [("background-color", "red")]}
    if f == "highlight_min":
        df = -df
    result = getattr(df.style, f)(**kwargs)._compute().ctx
    assert result == expected

