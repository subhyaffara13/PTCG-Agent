
def test_no_exponentiation():
    # if this passes, Pow.as_numer_denom should recognize
    # MatAdd as exponent
    raises(NotImplementedError, lambda: 3**(-2*C))

