
def test_tuple_correct_keyerror():
    # https://github.com/pandas-dev/pandas/issues/18798
    df = DataFrame(1, index=range(3), columns=MultiIndex.from_product([[1, 2], [3, 4]]))
    with pytest.raises(KeyError, match=r"^\(7, 8\)$"):
        df.groupby((7, 8)).mean()

