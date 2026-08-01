
def test_difference_sort_incomparable_true():
    idx = MultiIndex.from_product([[1, pd.Timestamp("2000"), 2], ["a", "b"]])
    other = MultiIndex.from_product([[3, pd.Timestamp("2000"), 4], ["c", "d"]])

    # TODO: this is raising in constructing a Categorical when calling
    #  algos.safe_sort. Should we catch and re-raise with a better message?
    msg = "'values' is not ordered, please explicitly specify the categories order "
    with pytest.raises(TypeError, match=msg):
        idx.difference(other, sort=True)

