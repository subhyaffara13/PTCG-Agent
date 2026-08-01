
def test_expand_func():
    # evaluation at 1 of Gauss' hypergeometric function:
    from sympy.abc import a, b, c
    from sympy.core.function import expand_func
    a1, b1, c1 = randcplx(), randcplx(), randcplx() + 5
    assert expand_func(hyper([a, b], [c], 1)) == \
        gamma(c)*gamma(-a - b + c)/(gamma(-a + c)*gamma(-b + c))
    assert abs(expand_func(hyper([a1, b1], [c1], 1)).n()
               - hyper([a1, b1], [c1], 1).n()) < 1e-10

    # hyperexpand wrapper for hyper:
    assert expand_func(hyper([], [], z)) == exp(z)
    assert expand_func(hyper([1, 2, 3], [], z)) == hyper([1, 2, 3], [], z)
    assert expand_func(meijerg([[1, 1], []], [[1], [0]], z)) == log(z + 1)
    assert expand_func(meijerg([[1, 1], []], [[], []], z)) == \
        meijerg([[1, 1], []], [[], []], z)

