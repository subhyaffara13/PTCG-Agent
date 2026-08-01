
def test_bad_association_args():
    # Invalid Test Statistic
    assert_raises(ValueError, association, [[1, 2], [3, 4]], "X")
    # Invalid array shape
    assert_raises(ValueError, association, [[[1, 2]], [[3, 4]]], "cramer")
    # chi2_contingency exception
    assert_raises(ValueError, association, [[-1, 10], [1, 2]], 'cramer')
    # Invalid Array Item Data Type
    assert_raises(ValueError, association,
                  np.array([[1, 2], ["dd", 4]], dtype=object), 'cramer')

