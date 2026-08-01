
def test_binomial_Mod():
    p, q = 10**5 + 3, 10**9 + 33 # prime modulo
    r = 10**7 + 5 # composite modulo

    # A few tests to get coverage
    # Lucas Theorem
    assert Mod(binomial(156675, 4433, evaluate=False), p) == Mod(binomial(156675, 4433), p)

    # factorial Mod
    assert Mod(binomial(1234, 432, evaluate=False), q) == Mod(binomial(1234, 432), q)

    # binomial factorize
    assert Mod(binomial(253, 113, evaluate=False), r) == Mod(binomial(253, 113), r)

    # using Granville's generalisation of Lucas' Theorem
    assert Mod(binomial(10**18, 10**12, evaluate=False), p*p) == 3744312326

