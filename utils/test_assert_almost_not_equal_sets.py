
def test_assert_almost_not_equal_sets():
    # GH#51727
    msg = r"{1, 2, 3} != {1, 2, 4}"
    with pytest.raises(AssertionError, match=msg):
        _assert_almost_equal_both({1, 2, 3}, {1, 2, 4})

