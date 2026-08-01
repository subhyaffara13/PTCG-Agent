
def test_torational_factor_list():
    p = expand(((x**2-1)*(x-2)).subs({x:x*(1 + sqrt(2))}))
    assert _torational_factor_list(p, x) == (-2, [
        (-x*(1 + sqrt(2))/2 + 1, 1),
        (-x*(1 + sqrt(2)) - 1, 1),
        (-x*(1 + sqrt(2)) + 1, 1)])


    p = expand(((x**2-1)*(x-2)).subs({x:x*(1 + 2**Rational(1, 4))}))
    assert _torational_factor_list(p, x) is None

