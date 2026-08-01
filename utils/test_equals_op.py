
def test_equals_op(idx):
    # GH9947, GH10637
    index_a = idx

    n = len(index_a)
    index_b = index_a[0:-1]
    index_c = index_a[0:-1].append(index_a[-2:-1])
    index_d = index_a[0:1]
    with pytest.raises(ValueError, match="Lengths must match"):
        index_a == index_b
    expected1 = np.array([True] * n)
    expected2 = np.array([True] * (n - 1) + [False])
    tm.assert_numpy_array_equal(index_a == index_a, expected1)
    tm.assert_numpy_array_equal(index_a == index_c, expected2)

    # test comparisons with numpy arrays
    array_a = np.array(index_a)
    array_b = np.array(index_a[0:-1])
    array_c = np.array(index_a[0:-1].append(index_a[-2:-1]))
    array_d = np.array(index_a[0:1])
    with pytest.raises(ValueError, match="Lengths must match"):
        index_a == array_b
    tm.assert_numpy_array_equal(index_a == array_a, expected1)
    tm.assert_numpy_array_equal(index_a == array_c, expected2)

    # test comparisons with Series
    series_a = Series(array_a)
    series_b = Series(array_b)
    series_c = Series(array_c)
    series_d = Series(array_d)
    with pytest.raises(ValueError, match="Lengths must match"):
        index_a == series_b

    tm.assert_series_equal(index_a == series_a, Series(expected1))
    tm.assert_series_equal(index_a == series_c, Series(expected2))

    # cases where length is 1 for one of them
    with pytest.raises(ValueError, match="Lengths must match"):
        index_a == index_d
    with pytest.raises(ValueError, match="Lengths must match"):
        index_a == series_d
    with pytest.raises(ValueError, match="Lengths must match"):
        index_a == array_d
    msg = "Can only compare identically-labeled Series objects"
    with pytest.raises(ValueError, match=msg):
        series_a == series_d
    with pytest.raises(ValueError, match="Lengths must match"):
        series_a == array_d

    # comparing with a scalar should broadcast; note that we are excluding
    # MultiIndex because in this case each item in the index is a tuple of
    # length 2, and therefore is considered an array of length 2 in the
    # comparison instead of a scalar
    if not isinstance(index_a, MultiIndex):
        expected3 = np.array([False] * (len(index_a) - 2) + [True, False])
        # assuming the 2nd to last item is unique in the data
        item = index_a[-2]
        tm.assert_numpy_array_equal(index_a == item, expected3)
        tm.assert_series_equal(series_a == item, Series(expected3))

