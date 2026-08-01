
def test_prime():
    assert prime(1) == 2
    assert prime(2) == 3
    assert prime(5) == 11
    assert prime(11) == 31
    assert prime(57) == 269
    assert prime(296) == 1949
    assert prime(559) == 4051
    assert prime(3000) == 27449
    assert prime(4096) == 38873
    assert prime(9096) == 94321
    assert prime(25023) == 287341
    assert prime(10000000) == 179424673 # issue #20951
    assert prime(99999999) == 2038074739
    raises(ValueError, lambda: prime(0))
    sieve.extend(3000)
    assert prime(401) == 2749
    raises(ValueError, lambda: prime(-1))


def test_prime():
    assert S.NegativeOne.is_prime is False
    assert S(-2).is_prime is False
    assert S(-4).is_prime is False
    assert S.Zero.is_prime is False
    assert S.One.is_prime is False
    assert S(2).is_prime is True
    assert S(17).is_prime is True
    assert S(4).is_prime is False


def test_prime():
    assert ask(Q.prime(x), Q.prime(x)) is True
    assert ask(Q.prime(x), ~Q.prime(x)) is False
    assert ask(Q.prime(x), Q.integer(x)) is None
    assert ask(Q.prime(x), ~Q.integer(x)) is False

    assert ask(Q.prime(2*x), Q.integer(x)) is None
    assert ask(Q.prime(x*y)) is None
    assert ask(Q.prime(x*y), Q.prime(x)) is None
    assert ask(Q.prime(x*y), Q.integer(x) & Q.integer(y)) is None
    assert ask(Q.prime(4*x), Q.integer(x)) is False
    assert ask(Q.prime(4*x)) is None

    assert ask(Q.prime(x**2), Q.integer(x)) is False
    assert ask(Q.prime(x**2), Q.prime(x)) is False

    # https://github.com/sympy/sympy/issues/27446
    assert ask(Q.prime(4**x), Q.integer(x)) is False
    assert ask(Q.prime(p**x), Q.prime(p) & Q.integer(x) & Q.ne(x, 1)) is False
    assert ask(Q.prime(n**x), Q.integer(x) & Q.composite(n)) is False
    assert ask(Q.prime(x**y), Q.integer(x) & Q.integer(y)) is None
    assert ask(Q.prime(2**x), Q.integer(x)) is None
    assert ask(Q.prime(p**x), Q.prime(p) & Q.integer(x)) is None

    # Ideally, these should return True since the base is prime and the exponent is one,
    # but currently, they return None.
    assert ask(Q.prime(x**y), Q.prime(x) & Q.eq(y,1)) is None
    assert ask(Q.prime(x**y), Q.prime(x) & Q.integer(y) & Q.gt(y,0) & Q.lt(y,2)) is None

    assert ask(Q.prime(Pow(x,1, evaluate=False)), Q.prime(x)) is True


def test_prime():
    assert satask(Q.prime(5)) is True
    assert satask(Q.prime(6)) is False
    assert satask(Q.prime(-5)) is False

    assert satask(Q.prime(x*y), Q.integer(x) & Q.integer(y)) is None
    assert satask(Q.prime(x*y), Q.prime(x) & Q.prime(y)) is False

