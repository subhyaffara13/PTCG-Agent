
def test_karr_convention():
    # Test the Karr product convention that we want to hold.
    # See his paper "Summation in Finite Terms" for a detailed
    # reasoning why we really want exactly this definition.
    # The convention is described for sums on page 309 and
    # essentially in section 1.4, definition 3. For products
    # we can find in analogy:
    #
    # \prod_{m <= i < n} f(i) 'has the obvious meaning'      for m < n
    # \prod_{m <= i < n} f(i) = 0                            for m = n
    # \prod_{m <= i < n} f(i) = 1 / \prod_{n <= i < m} f(i)  for m > n
    #
    # It is important to note that he defines all products with
    # the upper limit being *exclusive*.
    # In contrast, SymPy and the usual mathematical notation has:
    #
    # prod_{i = a}^b f(i) = f(a) * f(a+1) * ... * f(b-1) * f(b)
    #
    # with the upper limit *inclusive*. So translating between
    # the two we find that:
    #
    # \prod_{m <= i < n} f(i) = \prod_{i = m}^{n-1} f(i)
    #
    # where we intentionally used two different ways to typeset the
    # products and its limits.

    i = Symbol("i", integer=True)
    k = Symbol("k", integer=True)
    j = Symbol("j", integer=True, positive=True)

    # A simple example with a concrete factors and symbolic limits.

    # The normal product: m = k and n = k + j and therefore m < n:
    m = k
    n = k + j

    a = m
    b = n - 1
    S1 = Product(i**2, (i, a, b)).doit()

    # The reversed product: m = k + j and n = k and therefore m > n:
    m = k + j
    n = k

    a = m
    b = n - 1
    S2 = Product(i**2, (i, a, b)).doit()

    assert S1 * S2 == 1

    # Test the empty product: m = k and n = k and therefore m = n:
    m = k
    n = k

    a = m
    b = n - 1
    Sz = Product(i**2, (i, a, b)).doit()

    assert Sz == 1

    # Another example this time with an unspecified factor and
    # numeric limits. (We can not do both tests in the same example.)
    f = Function("f")

    # The normal product with m < n:
    m = 2
    n = 11

    a = m
    b = n - 1
    S1 = Product(f(i), (i, a, b)).doit()

    # The reversed product with m > n:
    m = 11
    n = 2

    a = m
    b = n - 1
    S2 = Product(f(i), (i, a, b)).doit()

    assert simplify(S1 * S2) == 1

    # Test the empty product with m = n:
    m = 5
    n = 5

    a = m
    b = n - 1
    Sz = Product(f(i), (i, a, b)).doit()

    assert Sz == 1


def test_karr_convention():
    # Test the Karr summation convention that we want to hold.
    # See his paper "Summation in Finite Terms" for a detailed
    # reasoning why we really want exactly this definition.
    # The convention is described on page 309 and essentially
    # in section 1.4, definition 3:
    #
    # \sum_{m <= i < n} f(i) 'has the obvious meaning'   for m < n
    # \sum_{m <= i < n} f(i) = 0                         for m = n
    # \sum_{m <= i < n} f(i) = - \sum_{n <= i < m} f(i)  for m > n
    #
    # It is important to note that he defines all sums with
    # the upper limit being *exclusive*.
    # In contrast, SymPy and the usual mathematical notation has:
    #
    # sum_{i = a}^b f(i) = f(a) + f(a+1) + ... + f(b-1) + f(b)
    #
    # with the upper limit *inclusive*. So translating between
    # the two we find that:
    #
    # \sum_{m <= i < n} f(i) = \sum_{i = m}^{n-1} f(i)
    #
    # where we intentionally used two different ways to typeset the
    # sum and its limits.

    i = Symbol("i", integer=True)
    k = Symbol("k", integer=True)
    j = Symbol("j", integer=True)

    # A simple example with a concrete summand and symbolic limits.

    # The normal sum: m = k and n = k + j and therefore m < n:
    m = k
    n = k + j

    a = m
    b = n - 1
    S1 = Sum(i**2, (i, a, b)).doit()

    # The reversed sum: m = k + j and n = k and therefore m > n:
    m = k + j
    n = k

    a = m
    b = n - 1
    S2 = Sum(i**2, (i, a, b)).doit()

    assert simplify(S1 + S2) == 0

    # Test the empty sum: m = k and n = k and therefore m = n:
    m = k
    n = k

    a = m
    b = n - 1
    Sz = Sum(i**2, (i, a, b)).doit()

    assert Sz == 0

    # Another example this time with an unspecified summand and
    # numeric limits. (We can not do both tests in the same example.)

    # The normal sum with m < n:
    m = 2
    n = 11

    a = m
    b = n - 1
    S1 = Sum(f(i), (i, a, b)).doit()

    # The reversed sum with m > n:
    m = 11
    n = 2

    a = m
    b = n - 1
    S2 = Sum(f(i), (i, a, b)).doit()

    assert simplify(S1 + S2) == 0

    # Test the empty sum with m = n:
    m = 5
    n = 5

    a = m
    b = n - 1
    Sz = Sum(f(i), (i, a, b)).doit()

    assert Sz == 0

    e = Piecewise((exp(-i), Mod(i, 2) > 0), (0, True))
    s = Sum(e, (i, 0, 11))
    assert s.n(3) == s.doit().n(3)

    # issue #27893
    n = Symbol('n', integer=True)
    assert Sum(1/(x**2 + 1), (x, oo, 0)).doit(deep=False) == Rational(-1, 2) + pi / (2 * tanh(pi))
    assert Sum(c**x/factorial(x), (x, oo, 0)).doit(deep=False).simplify() == exp(c) - 1 # exponential series
    assert Sum((-1)**x/x, (x, oo,0)).doit() == -log(2) # alternating harmnic series
    assert Sum((1/2)**x,(x, oo, -1)).doit() == S(2) # geometric series
    assert Sum(1/x, (x, oo, 0)).doit() == oo # harmonic series, divergent
    assert Sum((-1)**x/(2*x+1), (x, oo, -1)).doit() == pi/4 # leibniz series
    assert Sum((((-1)**x) * c**(2*x+1)) / factorial(2*x+1), (x, oo, -1)).doit() == sin(c) # sinusoidal series
    assert Sum((((-1)**x) * c**(2*x+1)) / (2*x+1), (x, 0, oo)).doit() \
        == Piecewise((atan(c), Ne(c**2, -1) & (Abs(c**2) <= 1)), \
                     (Sum((-1)**x*c**(2*x + 1)/(2*x + 1), (x, 0, oo)), True)) # arctangent series
    assert Sum(binomial(n, x) * c**x, (x, 0, oo)).doit() \
        == Piecewise(((c + 1)**n, \
                     ((n <= -1) & (Abs(c) < 1)) \
                        | ((n > 0) & (Abs(c) <= 1)) \
                        | ((n <= 0) & (n > -1) & Ne(c, -1) & (Abs(c) <= 1))), \
                     (Sum(c**x*binomial(n, x), (x, 0, oo)), True)) # binomial series
    assert Sum(1/x**n, (x, oo, 0)).doit() \
        == Piecewise((zeta(n), n > 1), (Sum(x**(-n), (x, oo, 0)), True)) # Euler's zeta function

