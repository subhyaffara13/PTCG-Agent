
def test_factorial():
    f = factorial(x)
    assert limit(f, x, oo) is oo
    assert limit(x/f, x, oo) == 0
    # see Stirling's approximation:
    # https://en.wikipedia.org/wiki/Stirling's_approximation
    assert limit(f/(sqrt(2*pi*x)*(x/E)**x), x, oo) == 1
    assert limit(f, x, -oo) == gamma(-oo)


def test_factorial():
    n = sy.Symbol('n')
    assert aesara_code_(sy.factorial(n))


def test_factorial():
    n = Symbol('n', integer=True)
    assert str(factorial(-2)) == "zoo"
    assert str(factorial(0)) == "1"
    assert str(factorial(7)) == "5040"
    assert str(factorial(n)) == "factorial(n)"
    assert str(factorial(2*n)) == "factorial(2*n)"
    assert str(factorial(factorial(n))) == 'factorial(factorial(n))'
    assert str(factorial(factorial2(n))) == 'factorial(factorial2(n))'
    assert str(factorial2(factorial(n))) == 'factorial2(factorial(n))'
    assert str(factorial2(factorial2(n))) == 'factorial2(factorial2(n))'
    assert str(subfactorial(3)) == "2"
    assert str(subfactorial(n)) == "subfactorial(n)"
    assert str(subfactorial(2*n)) == "subfactorial(2*n)"


def test_factorial():
    n = sy.Symbol('n')
    assert theano_code_(sy.factorial(n))


def test_factorial():
    x = Symbol('x')
    n = Symbol('n', integer=True)
    k = Symbol('k', integer=True, nonnegative=True)
    r = Symbol('r', integer=False)
    s = Symbol('s', integer=False, negative=True)
    t = Symbol('t', nonnegative=True)
    u = Symbol('u', noninteger=True)

    assert factorial(-2) is zoo
    assert factorial(0) == 1
    assert factorial(7) == 5040
    assert factorial(19) == 121645100408832000
    assert factorial(31) == 8222838654177922817725562880000000
    assert factorial(n).func == factorial
    assert factorial(2*n).func == factorial

    assert factorial(x).is_integer is None
    assert factorial(n).is_integer is None
    assert factorial(k).is_integer
    assert factorial(r).is_integer is None

    assert factorial(n).is_positive is None
    assert factorial(k).is_positive

    assert factorial(x).is_real is None
    assert factorial(n).is_real is None
    assert factorial(k).is_real is True
    assert factorial(r).is_real is None
    assert factorial(s).is_real is True
    assert factorial(t).is_real is True
    assert factorial(u).is_real is True

    assert factorial(x).is_composite is None
    assert factorial(n).is_composite is None
    assert factorial(k).is_composite is None
    assert factorial(k + 3).is_composite is True
    assert factorial(r).is_composite is None
    assert factorial(s).is_composite is None
    assert factorial(t).is_composite is None
    assert factorial(u).is_composite is None

    assert factorial(oo) is oo

