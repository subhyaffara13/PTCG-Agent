
def test_select_bad_cols(key, test_frame):
    g = test_frame.resample("h")
    # 'A' should not be referenced as a bad column...
    # will have to rethink regex if you change message!
    msg = r"^\"Columns not found: 'D'\"$"
    with pytest.raises(KeyError, match=msg):
        g[key]


def test_select_bad_cols():
    df = DataFrame([[1, 2]], columns=["A", "B"])
    g = df.rolling(window=5)
    with pytest.raises(KeyError, match="Columns not found: 'C'"):
        g[["C"]]
    with pytest.raises(KeyError, match="^[^A]+$"):
        # A should not be referenced as a bad column...
        # will have to rethink regex if you change message!
        g[["A", "C"]]

