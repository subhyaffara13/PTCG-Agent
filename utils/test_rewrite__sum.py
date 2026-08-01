
def test_rewrite_Sum():
    assert Product(1 - S.Half**2/k**2, (k, 1, oo)).rewrite(Sum) == \
        exp(Sum(log(1 - 1/(4*k**2)), (k, 1, oo)))

