
def test_lambert_multivariate():
    from sympy.abc import x, y
    assert _filtered_gens(Poly(x + 1/x + exp(x) + y), x) == {x, exp(x)}
    assert _lambert(x, x) == []
    assert solve((x**2 - 2*x + 1).subs(x, log(x) + 3*x)) == [LambertW(3*S.Exp1)/3]
    assert solve((x**2 - 2*x + 1).subs(x, (log(x) + 3*x)**2 - 1)) == \
          [LambertW(3*exp(-sqrt(2)))/3, LambertW(3*exp(sqrt(2)))/3]
    assert solve((x**2 - 2*x - 2).subs(x, log(x) + 3*x)) == \
          [LambertW(3*exp(1 - sqrt(3)))/3, LambertW(3*exp(1 + sqrt(3)))/3]
    eq = (x*exp(x) - 3).subs(x, x*exp(x))
    assert solve(eq) == [LambertW(3*exp(-LambertW(3)))]
    # coverage test
    raises(NotImplementedError, lambda: solve(x - sin(x)*log(y - x), x))
    ans = [3, -3*LambertW(-log(3)/3)/log(3)]  # 3 and 2.478...
    assert solve(x**3 - 3**x, x) == ans
    assert set(solve(3*log(x) - x*log(3))) == set(ans)
    assert solve(LambertW(2*x) - y, x) == [y*exp(y)/2]

