
def test_Symbol():
    """ Test printing a Symbol to a aesara variable. """
    xx = aesara_code_(x)
    assert isinstance(xx, Variable)
    assert xx.broadcastable == ()
    assert xx.name == x.name

    xx2 = aesara_code_(x, broadcastables={x: (False,)})
    assert xx2.broadcastable == (False,)
    assert xx2.name == x.name


def test_Symbol():
    assert precedence(x) == PRECEDENCE["Atom"]


def test_Symbol():
    sT(x, "Symbol('x')")
    sT(y, "Symbol('y')")
    sT(Symbol('x', negative=True), "Symbol('x', negative=True)")


def test_Symbol():
    assert str(y) == "y"
    assert str(x) == "x"
    e = x
    assert str(e) == "x"


def test_Symbol():
    """ Test printing a Symbol to a theano variable. """
    xx = theano_code_(x)
    assert isinstance(xx, (tt.TensorVariable, ts.ScalarVariable))
    assert xx.broadcastable == ()
    assert xx.name == x.name

    xx2 = theano_code_(x, broadcastables={x: (False,)})
    assert xx2.broadcastable == (False,)
    assert xx2.name == x.name


def test_Symbol():
    e = a*b
    assert e == a*b
    assert a*b*b == a*b**2
    assert a*b*b + c == c + a*b**2
    assert a*b*b - c == -c + a*b**2

    x = Symbol('x', complex=True, real=False)
    assert x.is_imaginary is None  # could be I or 1 + I
    x = Symbol('x', complex=True, imaginary=False)
    assert x.is_real is None  # could be 1 or 1 + I
    x = Symbol('x', real=True)
    assert x.is_complex
    x = Symbol('x', imaginary=True)
    assert x.is_complex
    x = Symbol('x', real=False, imaginary=False)
    assert x.is_complex is None  # might be a non-number


def test_Symbol():
    a = Symbol("a")
    x1 = Symbol("x")
    x2 = Symbol("x")
    xdummy1 = Dummy("x")
    xdummy2 = Dummy("x")

    assert a != x1
    assert a != x2
    assert x1 == x2
    assert x1 != xdummy1
    assert xdummy1 != xdummy2

    assert Symbol("x") == Symbol("x")
    assert Dummy("x") != Dummy("x")
    d = symbols('d', cls=Dummy)
    assert isinstance(d, Dummy)
    c, d = symbols('c,d', cls=Dummy)
    assert isinstance(c, Dummy)
    assert isinstance(d, Dummy)
    raises(TypeError, lambda: Symbol())

