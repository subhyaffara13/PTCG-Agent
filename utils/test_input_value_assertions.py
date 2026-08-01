
def test_input_value_assertions():
    a, b = symbols('a b')
    p, q = symbols('p q', positive=True)
    m, n = symbols('m n', positive=False, real=True)

    raises(ValueError, lambda: Normal('x', 3, 0))
    raises(ValueError, lambda: Normal('x', m, n))
    Normal('X', a, p)  # No error raised
    raises(ValueError, lambda: Exponential('x', m))
    Exponential('Ex', p)  # No error raised
    for fn in [Pareto, Weibull, Beta, Gamma]:
        raises(ValueError, lambda: fn('x', m, p))
        raises(ValueError, lambda: fn('x', p, n))
        fn('x', p, q)  # No error raised

