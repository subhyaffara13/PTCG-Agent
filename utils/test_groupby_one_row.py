
def test_groupby_one_row():
    # GH 11741
    msg = r"^'Z'$"
    df1 = DataFrame(
        np.random.default_rng(2).standard_normal((1, 4)), columns=list("ABCD")
    )
    with pytest.raises(KeyError, match=msg):
        df1.groupby("Z")
    df2 = DataFrame(
        np.random.default_rng(2).standard_normal((2, 4)), columns=list("ABCD")
    )
    with pytest.raises(KeyError, match=msg):
        df2.groupby("Z")

