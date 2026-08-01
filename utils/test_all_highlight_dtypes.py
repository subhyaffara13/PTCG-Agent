
def test_all_highlight_dtypes(f, kwargs, dtype):
    df = DataFrame([[0, 10], [20, 30]], dtype=dtype)
    if f == "highlight_quantile" and isinstance(df.iloc[0, 0], (str)):
        return None  # quantile incompatible with str
    if f == "highlight_between":
        kwargs["left"] = df.iloc[1, 0]  # set the range low for testing

    expected = {(1, 0): [("background-color", "yellow")]}
    result = getattr(df.style, f)(**kwargs)._compute().ctx
    assert result == expected

