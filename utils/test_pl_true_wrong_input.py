
def test_pl_true_wrong_input():
    from sympy.core.numbers import pi
    raises(ValueError, lambda: pl_true('John Cleese'))
    raises(ValueError, lambda: pl_true(42 + pi + pi ** 2))
    raises(ValueError, lambda: pl_true(42))

