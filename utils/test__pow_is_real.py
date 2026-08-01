
def test_Pow_is_real():
    x = Symbol('x', real=True)
    y = Symbol('y', positive=True)

    assert (x**2).is_real is True
    assert (x**3).is_real is True
    assert (x**x).is_real is None
    assert (y**x).is_real is True

    assert (x**Rational(1, 3)).is_real is None
    assert (y**Rational(1, 3)).is_real is True

    assert sqrt(-1 - sqrt(2)).is_real is False

    i = Symbol('i', imaginary=True)
    assert (i**i).is_real is None
    assert (I**i).is_extended_real is True
    assert ((-I)**i).is_extended_real is True
    assert (2**i).is_real is None  # (2**(pi/log(2) * I)) is real, 2**I is not
    assert (2**I).is_real is False
    assert (2**-I).is_real is False
    assert (i**2).is_extended_real is True
    assert (i**3).is_extended_real is False
    assert (i**x).is_real is None  # could be (-I)**(2/3)
    e = Symbol('e', even=True)
    o = Symbol('o', odd=True)
    k = Symbol('k', integer=True)
    assert (i**e).is_extended_real is True
    assert (i**o).is_extended_real is False
    assert (i**k).is_real is None
    assert (i**(4*k)).is_extended_real is True

    x = Symbol("x", nonnegative=True)
    y = Symbol("y", nonnegative=True)
    assert im(x**y).expand(complex=True) is S.Zero
    assert (x**y).is_real is True
    i = Symbol('i', imaginary=True)
    assert (exp(i)**I).is_extended_real is True
    assert log(exp(i)).is_imaginary is None  # i could be 2*pi*I
    c = Symbol('c', complex=True)
    assert log(c).is_real is None  # c could be 0 or 2, too
    assert log(exp(c)).is_real is None  # log(0), log(E), ...
    n = Symbol('n', negative=False)
    assert log(n).is_real is None
    n = Symbol('n', nonnegative=True)
    assert log(n).is_real is None

    assert sqrt(-I).is_real is False  # issue 7843

    i = Symbol('i', integer=True)
    assert (1/(i-1)).is_real is None
    assert (1/(i-1)).is_extended_real is None

    # test issue 20715
    from sympy.core.parameters import evaluate
    x = S(-1)
    with evaluate(False):
        assert x.is_negative is True

    f = Pow(x, -1)
    with evaluate(False):
        assert f.is_imaginary is False

