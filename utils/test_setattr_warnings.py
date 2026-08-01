
def test_setattr_warnings():
    # GH7175 - GOTCHA: You can't use dot notation to add a column...
    d = {
        "one": pd.Series([1.0, 2.0, 3.0], index=["a", "b", "c"]),
        "two": pd.Series([1.0, 2.0, 3.0, 4.0], index=["a", "b", "c", "d"]),
    }
    df = pd.DataFrame(d)

    with tm.assert_produces_warning(None):
        #  successfully add new column
        #  this should not raise a warning
        df["three"] = df.two + 1
        assert df.three.sum() > df.two.sum()

    with tm.assert_produces_warning(None):
        #  successfully modify column in place
        #  this should not raise a warning
        df.one += 1
        assert df.one.iloc[0] == 2

    with tm.assert_produces_warning(None):
        #  successfully add an attribute to a series
        #  this should not raise a warning
        df.two.not_an_index = [1, 2]

    with tm.assert_produces_warning(UserWarning, match="doesn't allow columns"):
        #  warn when setting column to nonexistent name
        df.four = df.two + 2
        assert df.four.sum() > df.two.sum()

