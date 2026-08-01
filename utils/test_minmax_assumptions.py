
def test_minmax_assumptions():
    r = Symbol('r', real=True)
    a = Symbol('a', real=True, algebraic=True)
    t = Symbol('t', real=True, transcendental=True)
    q = Symbol('q', rational=True)
    p = Symbol('p', irrational=True)
    n = Symbol('n', rational=True, integer=False)
    i = Symbol('i', integer=True)
    o = Symbol('o', odd=True)
    e = Symbol('e', even=True)
    k = Symbol('k', prime=True)
    reals = [r, a, t, q, p, n, i, o, e, k]

    for ext in (Max, Min):
        for x, y in it.product(reals, repeat=2):

            # Must be real
            assert ext(x, y).is_real

            # Algebraic?
            if x.is_algebraic and y.is_algebraic:
                assert ext(x, y).is_algebraic
            elif x.is_transcendental and y.is_transcendental:
                assert ext(x, y).is_transcendental
            else:
                assert ext(x, y).is_algebraic is None

            # Rational?
            if x.is_rational and y.is_rational:
                assert ext(x, y).is_rational
            elif x.is_irrational and y.is_irrational:
                assert ext(x, y).is_irrational
            else:
                assert ext(x, y).is_rational is None

            # Integer?
            if x.is_integer and y.is_integer:
                assert ext(x, y).is_integer
            elif x.is_noninteger and y.is_noninteger:
                assert ext(x, y).is_noninteger
            else:
                assert ext(x, y).is_integer is None

            # Odd?
            if x.is_odd and y.is_odd:
                assert ext(x, y).is_odd
            elif x.is_odd is False and y.is_odd is False:
                assert ext(x, y).is_odd is False
            else:
                assert ext(x, y).is_odd is None

            # Even?
            if x.is_even and y.is_even:
                assert ext(x, y).is_even
            elif x.is_even is False and y.is_even is False:
                assert ext(x, y).is_even is False
            else:
                assert ext(x, y).is_even is None

            # Prime?
            if x.is_prime and y.is_prime:
                assert ext(x, y).is_prime
            elif x.is_prime is False and y.is_prime is False:
                assert ext(x, y).is_prime is False
            else:
                assert ext(x, y).is_prime is None

