
def test_sympify_flint():
    if _flint is not None:
        import flint

        value = sympify(flint.fmpz(1000001))
        assert value == Integer(1000001) and type(value) is Integer

        value = sympify(flint.fmpq(101, 127))
        assert value == Rational(101, 127) and type(value) is Rational

