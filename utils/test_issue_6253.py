
def test_issue_6253():
    # Note: this used to raise NotImplementedError
    # Note: psi in _check_antecedents becomes NaN.
    assert integrate((sqrt(1 - x) + sqrt(1 + x))**2/x, x, meijerg=True) == \
        Integral((sqrt(-x + 1) + sqrt(x + 1))**2/x, x)

