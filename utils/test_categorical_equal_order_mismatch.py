
def test_categorical_equal_order_mismatch(check_category_order):
    c1 = Categorical([1, 2, 3, 4], categories=[1, 2, 3, 4])
    c2 = Categorical([1, 2, 3, 4], categories=[4, 3, 2, 1])
    kwargs = {"check_category_order": check_category_order}

    if check_category_order:
        msg = """Categorical\\.categories are different

Categorical\\.categories values are different \\(100\\.0 %\\)
\\[left\\]:  Index\\(\\[1, 2, 3, 4\\], dtype='int64'\\)
\\[right\\]: Index\\(\\[4, 3, 2, 1\\], dtype='int64'\\)"""
        with pytest.raises(AssertionError, match=msg):
            tm.assert_categorical_equal(c1, c2, **kwargs)
    else:
        tm.assert_categorical_equal(c1, c2, **kwargs)

