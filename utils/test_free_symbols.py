
def test_free_symbols():
    assert ConditionSet(x, Eq(y, 0), FiniteSet(z)
        ).free_symbols == {y, z}
    assert ConditionSet(x, Eq(x, 0), FiniteSet(z)
        ).free_symbols == {z}
    assert ConditionSet(x, Eq(x, 0), FiniteSet(x, z)
        ).free_symbols == {x, z}
    assert ConditionSet(x, Eq(x, 0), ImageSet(Lambda(y, y**2),
        S.Integers)).free_symbols == set()


def test_free_symbols():
    assert Order(1).free_symbols == set()
    assert Order(x).free_symbols == {x}
    assert Order(1, x).free_symbols == {x}
    assert Order(x*y).free_symbols == {x, y}
    assert Order(x, x, y).free_symbols == {x, y}


def test_free_symbols():
    assert PropertiesOnlyMatrix([[x], [0]]).free_symbols == {x}


def test_free_symbols():
    for M in ImmutableMatrix, ImmutableSparseMatrix, Matrix, SparseMatrix:
        assert M([[x], [0]]).free_symbols == {x}


def test_free_symbols():
    for M in ImmutableMatrix, ImmutableSparseMatrix, Matrix, SparseMatrix:
        assert M([[x], [0]]).free_symbols == {x}


def test_free_symbols():
    assert (C*D).free_symbols == {C, D}


def test_free_symbols():
    from sympy.abc import x, y, z
    assert Integral(0, x).free_symbols == {x}
    assert Integral(x).free_symbols == {x}
    assert Integral(x, (x, None, y)).free_symbols == {y}
    assert Integral(x, (x, y, None)).free_symbols == {y}
    assert Integral(x, (x, 1, y)).free_symbols == {y}
    assert Integral(x, (x, y, 1)).free_symbols == {y}
    assert Integral(x, (x, x, y)).free_symbols == {x, y}
    assert Integral(x, x, y).free_symbols == {x, y}
    assert Integral(x, (x, 1, 2)).free_symbols == set()
    assert Integral(x, (y, 1, 2)).free_symbols == {x}
    # pseudo-free in this case
    assert Integral(x, (y, z, z)).free_symbols == {x, z}
    assert Integral(x, (y, 1, 2), (y, None, None)
        ).free_symbols == {x, y}
    assert Integral(x, (y, 1, 2), (x, 1, y)
        ).free_symbols == {y}
    assert Integral(2, (y, 1, 2), (y, 1, x), (x, 1, 2)
        ).free_symbols == set()
    assert Integral(2, (y, x, 2), (y, 1, x), (x, 1, 2)
        ).free_symbols == set()
    assert Integral(2, (x, 1, 2), (y, x, 2), (y, 1, 2)
        ).free_symbols == {x}
    assert Integral(f(x), (f(x), 1, y)).free_symbols == {y}
    assert Integral(f(x), (f(x), 1, x)).free_symbols == {x}


def test_free_symbols():
    f = Function('f')
    assert mellin_transform(f(x), x, s).free_symbols == {s}
    assert mellin_transform(f(x)*a, x, s).free_symbols == {s, a}


def test_free_symbols():
    a, b, c, d, e, f, s = symbols('a:f,s')
    assert Point(a, b).free_symbols == {a, b}
    assert Line((a, b), (c, d)).free_symbols == {a, b, c, d}
    assert Ray((a, b), (c, d)).free_symbols == {a, b, c, d}
    assert Ray((a, b), angle=c).free_symbols == {a, b, c}
    assert Segment((a, b), (c, d)).free_symbols == {a, b, c, d}
    assert Line((a, b), slope=c).free_symbols == {a, b, c}
    assert Curve((a*s, b*s), (s, c, d)).free_symbols == {a, b, c, d}
    assert Ellipse((a, b), c, d).free_symbols == {a, b, c, d}
    assert Ellipse((a, b), c, eccentricity=d).free_symbols == \
        {a, b, c, d}
    assert Ellipse((a, b), vradius=c, eccentricity=d).free_symbols == \
        {a, b, c, d}
    assert Circle((a, b), c).free_symbols == {a, b, c}
    assert Circle((a, b), (c, d), (e, f)).free_symbols == \
        {e, d, c, b, f, a}
    assert Polygon((a, b), (c, d), (e, f)).free_symbols == \
        {e, b, d, f, a, c}
    assert RegularPolygon((a, b), c, d, e).free_symbols == {e, a, b, c, d}


def test_free_symbols():
    # free_symbols should return the free symbols of an object
    assert S.One.free_symbols == set()
    assert x.free_symbols == {x}
    assert Integral(x, (x, 1, y)).free_symbols == {y}
    assert (-Integral(x, (x, 1, y))).free_symbols == {y}
    assert meter.free_symbols == set()
    assert (meter**x).free_symbols == {x}


def test_free_symbols():
    for func in [Sum, Product]:
        assert func(1, (x, 1, 2)).free_symbols == set()
        assert func(0, (x, 1, y)).free_symbols == {y}
        assert func(2, (x, 1, y)).free_symbols == {y}
        assert func(x, (x, 1, 2)).free_symbols == set()
        assert func(x, (x, 1, y)).free_symbols == {y}
        assert func(x, (y, 1, y)).free_symbols == {x, y}
        assert func(x, (y, 1, 2)).free_symbols == {x}
        assert func(x, (y, 1, 1)).free_symbols == {x}
        assert func(x, (y, 1, z)).free_symbols == {x, z}
        assert func(x, (x, 1, y), (y, 1, 2)).free_symbols == set()
        assert func(x, (x, 1, y), (y, 1, z)).free_symbols == {z}
        assert func(x, (x, 1, y), (y, 1, y)).free_symbols == {y}
        assert func(x, (y, 1, y), (y, 1, z)).free_symbols == {x, z}
    assert Sum(1, (x, 1, y)).free_symbols == {y}
    # free_symbols answers whether the object *as written* has free symbols,
    # not whether the evaluated expression has free symbols
    assert Product(1, (x, 1, y)).free_symbols == {y}
    # don't count free symbols that are not independent of integration
    # variable(s)
    assert func(f(x), (f(x), 1, 2)).free_symbols == set()
    assert func(f(x), (f(x), 1, x)).free_symbols == {x}
    assert func(f(x), (f(x), 1, y)).free_symbols == {y}
    assert func(f(x), (z, 1, y)).free_symbols == {x, y}

