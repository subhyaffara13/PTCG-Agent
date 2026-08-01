
def test_equals():
    assert Not(Or(A, B)).equals(And(Not(A), Not(B))) is True
    assert Equivalent(A, B).equals((A >> B) & (B >> A)) is True
    assert ((A | ~B) & (~A | B)).equals((~A & ~B) | (A & B)) is True
    assert (A >> B).equals(~A >> ~B) is False
    assert (A >> (B >> A)).equals(A >> (C >> A)) is False
    raises(NotImplementedError, lambda: (A & B).equals(A > B))


def test_equals():
    p1 = Point(0, 0)
    p2 = Point(1, 1)

    l1 = Line(p1, p2)
    l2 = Line((0, 5), slope=m)
    l3 = Line(Point(x1, x1), Point(x1, 1 + x1))

    assert l1.perpendicular_line(p1.args).equals(Line(Point(0, 0), Point(1, -1)))
    assert l1.perpendicular_line(p1).equals(Line(Point(0, 0), Point(1, -1)))
    assert Line(Point(x1, x1), Point(y1, y1)).parallel_line(Point(-x1, x1)). \
        equals(Line(Point(-x1, x1), Point(-y1, 2 * x1 - y1)))
    assert l3.parallel_line(p1.args).equals(Line(Point(0, 0), Point(0, -1)))
    assert l3.parallel_line(p1).equals(Line(Point(0, 0), Point(0, -1)))
    assert (l2.distance(Point(2, 3)) - 2 * abs(m + 1) / sqrt(m ** 2 + 1)).equals(0)
    assert Line3D(p1, Point3D(0, 1, 0)).equals(Point(1.0, 1.0)) is False
    assert Line3D(Point3D(0, 0, 0), Point3D(1, 0, 0)).equals(Line3D(Point3D(-5, 0, 0), Point3D(-1, 0, 0))) is True
    assert Line3D(Point3D(0, 0, 0), Point3D(1, 0, 0)).equals(Line3D(p1, Point3D(0, 1, 0))) is False
    assert Ray3D(p1, Point3D(0, 0, -1)).equals(Point(1.0, 1.0)) is False
    assert Ray3D(p1, Point3D(0, 0, -1)).equals(Ray3D(p1, Point3D(0, 0, -1))) is True
    assert Line3D((0, 0), (t, t)).perpendicular_line(Point(0, 1, 0)).equals(
        Line3D(Point3D(0, 1, 0), Point3D(S.Half, S.Half, 0)))
    assert Line3D((0, 0), (t, t)).perpendicular_segment(Point(0, 1, 0)).equals(Segment3D((0, 1), (S.Half, S.Half)))
    assert Line3D(p1, Point3D(0, 1, 0)).equals(Point(1.0, 1.0)) is False


def test_equals():
    assert (-3 - sqrt(5) + (-sqrt(10)/2 - sqrt(2)/2)**2).equals(0)
    assert (x**2 - 1).equals((x + 1)*(x - 1))
    assert (cos(x)**2 + sin(x)**2).equals(1)
    assert (a*cos(x)**2 + a*sin(x)**2).equals(a)
    r = sqrt(2)
    assert (-1/(r + r*x) + 1/r/(1 + x)).equals(0)
    assert factorial(x + 1).equals((x + 1)*factorial(x))
    assert sqrt(3).equals(2*sqrt(3)) is False
    assert (sqrt(5)*sqrt(3)).equals(sqrt(3)) is False
    assert (sqrt(5) + sqrt(3)).equals(0) is False
    assert (sqrt(5) + pi).equals(0) is False
    assert meter.equals(0) is False
    assert (3*meter**2).equals(0) is False
    eq = -(-1)**(S(3)/4)*6**(S.One/4) + (-6)**(S.One/4)*I
    if eq != 0:  # if canonicalization makes this zero, skip the test
        assert eq.equals(0)
    assert sqrt(x).equals(0) is False

    # from integrate(x*sqrt(1 + 2*x), x);
    # diff is zero only when assumptions allow
    i = 2*sqrt(2)*x**(S(5)/2)*(1 + 1/(2*x))**(S(5)/2)/5 + \
        2*sqrt(2)*x**(S(3)/2)*(1 + 1/(2*x))**(S(5)/2)/(-6 - 3/x)
    ans = sqrt(2*x + 1)*(6*x**2 + x - 1)/15
    diff = i - ans
    assert diff.equals(0) is None  # should be False, but previously this was False due to wrong intermediate result
    assert diff.subs(x, Rational(-1, 2)/2) == 7*sqrt(2)/120
    # there are regions for x for which the expression is True, for
    # example, when x < -1/2 or x > 0 the expression is zero
    p = Symbol('p', positive=True)
    assert diff.subs(x, p).equals(0) is True
    assert diff.subs(x, -1).equals(0) is True

    # prove via minimal_polynomial or self-consistency
    eq = sqrt(1 + sqrt(3)) + sqrt(3 + 3*sqrt(3)) - sqrt(10 + 6*sqrt(3))
    assert eq.equals(0)
    q = 3**Rational(1, 3) + 3
    p = expand(q**3)**Rational(1, 3)
    assert (p - q).equals(0)

    # issue 6829
    # eq = q*x + q/4 + x**4 + x**3 + 2*x**2 - S.One/3
    # z = eq.subs(x, solve(eq, x)[0])
    q = symbols('q')
    z = (q*(-sqrt(-2*(-(q - S(7)/8)**S(2)/8 - S(2197)/13824)**(S.One/3) -
    S(13)/12)/2 - sqrt((2*q - S(7)/4)/sqrt(-2*(-(q - S(7)/8)**S(2)/8 -
    S(2197)/13824)**(S.One/3) - S(13)/12) + 2*(-(q - S(7)/8)**S(2)/8 -
    S(2197)/13824)**(S.One/3) - S(13)/6)/2 - S.One/4) + q/4 + (-sqrt(-2*(-(q
    - S(7)/8)**S(2)/8 - S(2197)/13824)**(S.One/3) - S(13)/12)/2 - sqrt((2*q
    - S(7)/4)/sqrt(-2*(-(q - S(7)/8)**S(2)/8 - S(2197)/13824)**(S.One/3) -
    S(13)/12) + 2*(-(q - S(7)/8)**S(2)/8 - S(2197)/13824)**(S.One/3) -
    S(13)/6)/2 - S.One/4)**4 + (-sqrt(-2*(-(q - S(7)/8)**S(2)/8 -
    S(2197)/13824)**(S.One/3) - S(13)/12)/2 - sqrt((2*q -
    S(7)/4)/sqrt(-2*(-(q - S(7)/8)**S(2)/8 - S(2197)/13824)**(S.One/3) -
    S(13)/12) + 2*(-(q - S(7)/8)**S(2)/8 - S(2197)/13824)**(S.One/3) -
    S(13)/6)/2 - S.One/4)**3 + 2*(-sqrt(-2*(-(q - S(7)/8)**S(2)/8 -
    S(2197)/13824)**(S.One/3) - S(13)/12)/2 - sqrt((2*q -
    S(7)/4)/sqrt(-2*(-(q - S(7)/8)**S(2)/8 - S(2197)/13824)**(S.One/3) -
    S(13)/12) + 2*(-(q - S(7)/8)**S(2)/8 - S(2197)/13824)**(S.One/3) -
    S(13)/6)/2 - S.One/4)**2 - Rational(1, 3))
    assert z.equals(0)


def test_equals():
    w, x, y, z = symbols('w:z')
    f = Function('f')
    assert Eq(x, 1).equals(Eq(x*(y + 1) - x*y - x + 1, x))
    assert Eq(x, y).equals(x < y, True) == False
    assert Eq(x, f(1)).equals(Eq(x, f(2)), True) == f(1) - f(2)
    assert Eq(f(1), y).equals(Eq(f(2), y), True) == f(1) - f(2)
    assert Eq(x, f(1)).equals(Eq(f(2), x), True) == f(1) - f(2)
    assert Eq(f(1), x).equals(Eq(x, f(2)), True) == f(1) - f(2)
    assert Eq(w, x).equals(Eq(y, z), True) == False
    assert Eq(f(1), f(2)).equals(Eq(f(3), f(4)), True) == f(1) - f(3)
    assert (x < y).equals(y > x, True) == True
    assert (x < y).equals(y >= x, True) == False
    assert (x < y).equals(z < y, True) == False
    assert (x < y).equals(x < z, True) == False
    assert (x < f(1)).equals(x < f(2), True) == f(1) - f(2)
    assert (f(1) < x).equals(f(2) < x, True) == f(1) - f(2)


def test_equals(arr, idx):
    s1 = Series(arr, index=idx)
    s2 = s1.copy()
    assert s1.equals(s2)

    s1[1] = 9
    assert not s1.equals(s2)


def test_equals(idx):
    assert idx.equals(idx)
    assert idx.equals(idx.copy())
    assert idx.equals(idx.astype(object))
    assert idx.equals(idx.to_flat_index())
    assert idx.equals(idx.to_flat_index().astype("category"))

    assert not idx.equals(list(idx))
    assert not idx.equals(np.array(idx))

    same_values = Index(idx, dtype=object)
    assert idx.equals(same_values)
    assert same_values.equals(idx)

    if idx.nlevels == 1:
        # do not test MultiIndex
        assert not idx.equals(Series(idx))


def test_equals():
    # GH-30652
    # equals is generally tested in /tests/extension/base/methods, but this
    # specifically tests that two arrays of the same class but different dtype
    # do not evaluate equal
    a1 = pd.array([1, 2, None], dtype="Float64")
    a2 = pd.array([1, 2, None], dtype="Float32")
    assert a1.equals(a2) is False


def test_equals():
    # GH-30652
    # equals is generally tested in /tests/extension/base/methods, but this
    # specifically tests that two arrays of the same class but different dtype
    # do not evaluate equal
    a1 = pd.array([1, 2, None], dtype="Int64")
    a2 = pd.array([1, 2, None], dtype="Int32")
    assert a1.equals(a2) is False

