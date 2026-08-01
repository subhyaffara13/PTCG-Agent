
def test_factorial_rewrite():
    n = Symbol('n', integer=True)
    k = Symbol('k', integer=True, nonnegative=True)

    assert factorial(n).rewrite(gamma) == gamma(n + 1)
    _i = Dummy('i')
    assert factorial(k).rewrite(Product).dummy_eq(Product(_i, (_i, 1, k)))
    assert factorial(n).rewrite(Product) == factorial(n)

