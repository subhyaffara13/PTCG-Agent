
def test_Lambda():
    assert str(Lambda(d, d**2)) == "Lambda(_d, _d**2)"
    # issue 2908
    assert str(Lambda((), 1)) == "Lambda((), 1)"
    assert str(Lambda((), x)) == "Lambda((), x)"
    assert str(Lambda((x, y), x+y)) == "Lambda((x, y), x + y)"
    assert str(Lambda(((x, y),), x+y)) == "Lambda(((x, y),), x + y)"


def test_Lambda():
    e = Lambda(x, x**2)
    assert e(4) == 16
    assert e(x) == x**2
    assert e(y) == y**2

    assert Lambda((), 42)() == 42
    assert unchanged(Lambda, (), 42)
    assert Lambda((), 42) != Lambda((), 43)
    assert Lambda((), f(x))() == f(x)
    assert Lambda((), 42).nargs == FiniteSet(0)

    assert unchanged(Lambda, (x,), x**2)
    assert Lambda(x, x**2) == Lambda((x,), x**2)
    assert Lambda(x, x**2) != Lambda(x, x**2 + 1)
    assert Lambda((x, y), x**y) != Lambda((y, x), y**x)
    assert Lambda((x, y), x**y) != Lambda((x, y), y**x)

    assert Lambda((x, y), x**y)(x, y) == x**y
    assert Lambda((x, y), x**y)(3, 3) == 3**3
    assert Lambda((x, y), x**y)(x, 3) == x**3
    assert Lambda((x, y), x**y)(3, y) == 3**y
    assert Lambda(x, f(x))(x) == f(x)
    assert Lambda(x, x**2)(e(x)) == x**4
    assert e(e(x)) == x**4

    x1, x2 = (Indexed('x', i) for i in (1, 2))
    assert Lambda((x1, x2), x1 + x2)(x, y) == x + y

    assert Lambda((x, y), x + y).nargs == FiniteSet(2)

    p = x, y, z, t
    assert Lambda(p, t*(x + y + z))(*p) == t * (x + y + z)

    eq = Lambda(x, 2*x) + Lambda(y, 2*y)
    assert eq != 2*Lambda(x, 2*x)
    assert eq.as_dummy() == 2*Lambda(x, 2*x).as_dummy()
    assert Lambda(x, 2*x) not in [ Lambda(x, x) ]
    raises(BadSignatureError, lambda: Lambda(1, x))
    assert Lambda(x, 1)(1) is S.One

    raises(BadSignatureError, lambda: Lambda((x, x), x + 2))
    raises(BadSignatureError, lambda: Lambda(((x, x), y), x))
    raises(BadSignatureError, lambda: Lambda(((y, x), x), x))
    raises(BadSignatureError, lambda: Lambda(((y, 1), 2), x))

    with warns_deprecated_sympy():
        assert Lambda([x, y], x+y) == Lambda((x, y), x+y)

    flam = Lambda(((x, y),), x + y)
    assert flam((2, 3)) == 5
    flam = Lambda(((x, y), z), x + y + z)
    assert flam((2, 3), 1) == 6
    flam = Lambda((((x, y), z),), x + y + z)
    assert flam(((2, 3), 1)) == 6
    raises(BadArgumentsError, lambda: flam(1, 2, 3))
    flam = Lambda( (x,), (x, x))
    assert flam(1,) == (1, 1)
    assert flam((1,)) == ((1,), (1,))
    flam = Lambda( ((x,),), (x, x))
    raises(BadArgumentsError, lambda: flam(1))
    assert flam((1,)) == (1, 1)

    # Previously TypeError was raised so this is potentially needed for
    # backwards compatibility.
    assert issubclass(BadSignatureError, TypeError)
    assert issubclass(BadArgumentsError, TypeError)

    # These are tested to see they don't raise:
    hash(Lambda(x, 2*x))
    hash(Lambda(x, x))  # IdentityFunction subclass

