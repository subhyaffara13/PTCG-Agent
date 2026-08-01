
def test_numpy_compat(func):
    # see gh-12811
    df = DataFrame({"A": [1, 2, 1], "B": [1, 2, 3]})
    g = df.groupby("A")

    msg = "numpy operations are not valid with groupby"

    with pytest.raises(UnsupportedFunctionCall, match=msg):
        getattr(g, func)(1, 2, 3)
    with pytest.raises(UnsupportedFunctionCall, match=msg):
        getattr(g, func)(foo=1)

