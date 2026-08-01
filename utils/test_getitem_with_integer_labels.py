
def test_getitem_with_integer_labels():
    # integer indexes, be careful
    ser = Series(
        np.random.default_rng(2).standard_normal(10), index=list(range(0, 20, 2))
    )
    inds = [0, 2, 5, 7, 8]
    arr_inds = np.array([0, 2, 5, 7, 8])
    with pytest.raises(KeyError, match="not in index"):
        ser[inds]

    with pytest.raises(KeyError, match="not in index"):
        ser[arr_inds]

