
def test_iloc_getitem_labels():
    # this is basically regular indexing
    arr = np.random.default_rng(2).standard_normal((4, 3))
    df = DataFrame(
        arr,
        columns=[["i", "i", "j"], ["A", "A", "B"]],
        index=[["i", "i", "j", "k"], ["X", "X", "Y", "Y"]],
    )
    result = df.iloc[2, 2]
    expected = arr[2, 2]
    assert result == expected

