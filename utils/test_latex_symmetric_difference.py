
def test_latex_symmetric_difference():
    assert latex(SymmetricDifference(Interval(2, 5), Interval(4, 7),
                                     evaluate=False)) == \
        r'\left[2, 5\right] \triangle \left[4, 7\right]'

