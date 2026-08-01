
def test_issue_15560():
    a = MatrixSymbol('a', 1, 1)
    e = pretty(a*(KroneckerProduct(a, a)))
    result = 'a*(a x a)'
    assert e == result

