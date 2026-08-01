
def test_keep_coeff():
    u = Mul(2, x + 1, evaluate=False)
    assert _keep_coeff(S.One, x) == x
    assert _keep_coeff(S.NegativeOne, x) == -x
    assert _keep_coeff(S(1.0), x) == 1.0*x
    assert _keep_coeff(S(-1.0), x) == -1.0*x
    assert _keep_coeff(S.One, 2*x) == 2*x
    assert _keep_coeff(S(2), x/2) == x
    assert _keep_coeff(S(2), sin(x)) == 2*sin(x)
    assert _keep_coeff(S(2), x + 1) == u
    assert _keep_coeff(x, 1/x) == 1
    assert _keep_coeff(x + 1, S(2)) == u
    assert _keep_coeff(S.Half, S.One) == S.Half
    p = Pow(2, 3, evaluate=False)
    assert _keep_coeff(S(-1), p) == Mul(-1, p, evaluate=False)
    a = Add(2, p, evaluate=False)
    assert _keep_coeff(S.Half, a, clear=True
        ) == Mul(S.Half, a, evaluate=False)
    assert _keep_coeff(S.Half, a, clear=False
        ) == Add(1, Mul(S.Half, p, evaluate=False), evaluate=False)

