
def test_exp_summation():
    w = symbols("w")
    m, n, i, j = symbols("m n i j")
    expr = exp(Sum(w*i, (i, 0, n), (j, 0, m)))
    assert expr.expand() == Product(exp(w*i), (i, 0, n), (j, 0, m))

