
def test_Pow_is_nonpositive_nonnegative():
    x = Symbol('x', real=True)

    k = Symbol('k', integer=True, nonnegative=True)
    l = Symbol('l', integer=True, positive=True)
    n = Symbol('n', even=True)
    m = Symbol('m', odd=True)

    assert (x**(4*k)).is_nonnegative is True
    assert (2**x).is_nonnegative is True
    assert ((-2)**x).is_nonnegative is None
    assert ((-2)**n).is_nonnegative is True
    assert ((-2)**m).is_nonnegative is False

    assert (k**2).is_nonnegative is True
    assert (k**(-2)).is_nonnegative is None
    assert (k**k).is_nonnegative is True

    assert (k**x).is_nonnegative is None    # NOTE (0**x).is_real = U
    assert (l**x).is_nonnegative is True
    assert (l**x).is_positive is True
    assert ((-k)**x).is_nonnegative is None

    assert ((-k)**m).is_nonnegative is None

    assert (2**x).is_nonpositive is False
    assert ((-2)**x).is_nonpositive is None
    assert ((-2)**n).is_nonpositive is False
    assert ((-2)**m).is_nonpositive is True

    assert (k**2).is_nonpositive is None
    assert (k**(-2)).is_nonpositive is None

    assert (k**x).is_nonpositive is None
    assert ((-k)**x).is_nonpositive is None
    assert ((-k)**n).is_nonpositive is None


    assert (x**2).is_nonnegative is True
    i = symbols('i', imaginary=True)
    assert (i**2).is_nonpositive is True
    assert (i**4).is_nonpositive is False
    assert (i**3).is_nonpositive is False
    assert (I**i).is_nonnegative is True
    assert (exp(I)**i).is_nonnegative is True

    assert ((-l)**n).is_nonnegative is True
    assert ((-l)**m).is_nonpositive is True
    assert ((-k)**n).is_nonnegative is None
    assert ((-k)**m).is_nonpositive is None

