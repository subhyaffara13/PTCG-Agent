
def test_erfi_series():
    assert erfi(x).series(x, 0, 7) == 2*x/sqrt(pi) + \
        2*x**3/3/sqrt(pi) + x**5/5/sqrt(pi) + O(x**7)

    assert erfi(x).series(x, oo) == \
        (3/(4*x**5) + 1/(2*x**3) + 1/x + O(x**(-6), (x, oo)))*exp(x**2)/sqrt(pi) - I

