
def test_leading_term():
    from sympy.functions.special.gamma_functions import digamma
    assert O(1/digamma(1/x)) == O(1/log(x))


def test_leading_term():
    l = Symbol('l', positive=True)
    assert SingularityFunction(x, 3, 2).as_leading_term(x) == 0
    assert SingularityFunction(x, -2, 1).as_leading_term(x) == 2
    assert SingularityFunction(x, 0, 0).as_leading_term(x) == 1
    assert SingularityFunction(x, 0, 0).as_leading_term(x, cdir=-1) == 0
    assert SingularityFunction(x, 0, -1).as_leading_term(x) == 0
    assert SingularityFunction(x, 0, -2).as_leading_term(x) == 0
    assert SingularityFunction(x, 0, -3).as_leading_term(x) == 0
    assert SingularityFunction(x, 0, -4).as_leading_term(x) == 0
    assert (SingularityFunction(x + l, 0, 1)/2\
        - SingularityFunction(x + l, l/2, 1)\
        + SingularityFunction(x + l, l, 1)/2).as_leading_term(x) == -x/2


def test_leading_term():
    x = Symbol('x')
    assert cosh(x).as_leading_term(x) == 1
    assert coth(x).as_leading_term(x) == 1/x
    for func in [sinh, tanh]:
        assert func(x).as_leading_term(x) == x
    for func in [sinh, cosh, tanh, coth]:
        for ar in (1/x, S.Half):
            eq = func(ar)
            assert eq.as_leading_term(x) == eq
    for func in [csch, sech]:
        eq = func(S.Half)
        assert eq.as_leading_term(x) == eq

