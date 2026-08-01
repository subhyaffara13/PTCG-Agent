
def test_Pow_is_integer():
    x = Symbol('x')

    k = Symbol('k', integer=True)
    n = Symbol('n', integer=True, nonnegative=True)
    m = Symbol('m', integer=True, positive=True)

    assert (k**2).is_integer is True
    assert (k**(-2)).is_integer is None
    assert ((m + 1)**(-2)).is_integer is False
    assert (m**(-1)).is_integer is None  # issue 8580

    assert (2**k).is_integer is None
    assert (2**(-k)).is_integer is None

    assert (2**n).is_integer is True
    assert (2**(-n)).is_integer is None

    assert (2**m).is_integer is True
    assert (2**(-m)).is_integer is False

    assert (x**2).is_integer is None
    assert (2**x).is_integer is None

    assert (k**n).is_integer is True
    assert (k**(-n)).is_integer is None

    assert (k**x).is_integer is None
    assert (x**k).is_integer is None

    assert (k**(n*m)).is_integer is True
    assert (k**(-n*m)).is_integer is None

    assert sqrt(3).is_integer is False
    assert sqrt(.3).is_integer is False
    assert Pow(3, 2, evaluate=False).is_integer is True
    assert Pow(3, 0, evaluate=False).is_integer is True
    assert Pow(3, -2, evaluate=False).is_integer is False
    assert Pow(S.Half, 3, evaluate=False).is_integer is False
    # decided by re-evaluating
    assert Pow(3, S.Half, evaluate=False).is_integer is False
    assert Pow(3, S.Half, evaluate=False).is_integer is False
    assert Pow(4, S.Half, evaluate=False).is_integer is True
    assert Pow(S.Half, -2, evaluate=False).is_integer is True

    assert ((-1)**k).is_integer

    # issue 8641
    x = Symbol('x', real=True, integer=False)
    assert (x**2).is_integer is None

    # issue 10458
    x = Symbol('x', positive=True)
    assert (1/(x + 1)).is_integer is False
    assert (1/(-x - 1)).is_integer is False
    assert (-1/(x + 1)).is_integer is False
    # issue 23287
    assert (x**2/2).is_integer is None

    # issue 8648-like
    k = Symbol('k', even=True)
    assert (k**3/2).is_integer
    assert (k**3/8).is_integer
    assert (k**3/16).is_integer is None
    assert (2/k).is_integer is None
    assert (2/k**2).is_integer is False
    o = Symbol('o', odd=True)
    assert (k/o).is_integer is None
    o = Symbol('o', odd=True, prime=True)
    assert (k/o).is_integer is False

