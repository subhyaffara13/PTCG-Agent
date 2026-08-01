
def test_assert_almost_equal_sets():
    # GH#51727
    _assert_almost_equal_both({1, 2, 3}, {1, 2, 3})

