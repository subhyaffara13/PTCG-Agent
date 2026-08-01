
def test_invert_modular():
    n = Dummy('n', integer=True)
    from sympy.solvers.solveset import _invert_modular as invert_modular

    # no solutions
    assert invert_modular(Mod(x, 12), S(1)/2, n, x) == (x, S.EmptySet)
    # non invertible cases
    assert invert_modular(Mod(sin(x), 7), S(5), n, x) == (Mod(sin(x), 7), 5)
    assert invert_modular(Mod(exp(x), 7), S(5), n, x) == (Mod(exp(x), 7), 5)
    assert invert_modular(Mod(log(x), 7), S(5), n, x) == (Mod(log(x), 7), 5)
    # a is symbol
    assert dumeq(invert_modular(Mod(x, 7), S(5), n, x),
            (x, ImageSet(Lambda(n, 7*n + 5), S.Integers)))
    # a.is_Add
    assert dumeq(invert_modular(Mod(x + 8, 7), S(5), n, x),
            (x, ImageSet(Lambda(n, 7*n + 4), S.Integers)))
    assert invert_modular(Mod(x**2 + x, 7), S(5), n, x) == \
            (Mod(x**2 + x, 7), 5)
    # a.is_Mul
    assert dumeq(invert_modular(Mod(3*x, 7), S(5), n, x),
            (x, ImageSet(Lambda(n, 7*n + 4), S.Integers)))
    assert invert_modular(Mod((x + 1)*(x + 2), 7), S(5), n, x) == \
            (Mod((x + 1)*(x + 2), 7), 5)
    # a.is_Pow
    assert invert_modular(Mod(x**4, 7), S(5), n, x) == \
            (x, S.EmptySet)
    assert dumeq(invert_modular(Mod(3**x, 4), S(3), n, x),
            (x, ImageSet(Lambda(n, 2*n + 1), S.Naturals0)))
    assert dumeq(invert_modular(Mod(2**(x**2 + x + 1), 7), S(2), n, x),
            (x**2 + x + 1, ImageSet(Lambda(n, 3*n + 1), S.Naturals0)))
    assert invert_modular(Mod(sin(x)**4, 7), S(5), n, x) == (x, S.EmptySet)

