
def test_polylog_series():
    assert polylog(1, z).series(z, n=5) == z + z**2/2 + z**3/3 + z**4/4 + O(z**5)
    assert polylog(1, sqrt(z)).series(z, n=3) == z/2 + z**2/4 + sqrt(z)\
        + z**(S(3)/2)/3 + z**(S(5)/2)/5 + O(z**3)

    # https://github.com/sympy/sympy/issues/9497
    assert polylog(S(3)/2, -z).series(z, 0, 5) == -z + sqrt(2)*z**2/4\
        - sqrt(3)*z**3/9 + z**4/8 + O(z**5)

