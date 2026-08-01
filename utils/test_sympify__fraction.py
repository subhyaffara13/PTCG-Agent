
def test_sympify_Fraction():
    try:
        import fractions
    except ImportError:
        pass
    else:
        value = sympify(fractions.Fraction(101, 127))
        assert value == Rational(101, 127) and type(value) is Rational

