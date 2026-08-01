
def test_index_equal_value_order_mismatch(check_exact, rtol, check_order):
    idx1 = Index([1, 2, 3])
    idx2 = Index([3, 2, 1])

    msg = """Index are different

Index values are different \\(66\\.66667 %\\)
\\[left\\]:  Index\\(\\[1, 2, 3\\], dtype='int64'\\)
\\[right\\]: Index\\(\\[3, 2, 1\\], dtype='int64'\\)"""

    if check_order:
        with pytest.raises(AssertionError, match=msg):
            tm.assert_index_equal(
                idx1, idx2, check_exact=check_exact, rtol=rtol, check_order=True
            )
    else:
        tm.assert_index_equal(
            idx1, idx2, check_exact=check_exact, rtol=rtol, check_order=False
        )

