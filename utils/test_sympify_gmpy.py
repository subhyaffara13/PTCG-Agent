
def test_sympify_gmpy():
    if _gmpy is not None:
        import gmpy2

        value = sympify(gmpy2.mpz(1000001))
        assert value == Integer(1000001) and type(value) is Integer

        value = sympify(gmpy2.mpq(101, 127))
        assert value == Rational(101, 127) and type(value) is Rational

