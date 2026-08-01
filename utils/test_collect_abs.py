
def test_collect_abs():
    s = abs(x) + abs(y)
    assert collect_abs(s) == s
    assert unchanged(Mul, abs(x), abs(y))
    ans = Abs(x*y)
    assert isinstance(ans, Abs)
    assert collect_abs(abs(x)*abs(y)) == ans
    assert collect_abs(1 + exp(abs(x)*abs(y))) == 1 + exp(ans)

    # See https://github.com/sympy/sympy/issues/12910
    p = Symbol('p', positive=True)
    assert collect_abs(p/abs(1-p)).is_commutative is True

