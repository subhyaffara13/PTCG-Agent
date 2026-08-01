
def test_subs():
    rl = subs(1, 2)
    assert rl(1) == 2
    assert rl(3) == 3


def test_subs():
    from sympy.core.symbol import symbols
    a, b, c, d, e, f = symbols('a,b,c,d,e,f')
    mapping = {a: d, d: a, Basic(e): Basic(f)}
    expr = Basic(a, Basic(b, c), Basic(d, Basic(e)))
    result = Basic(d, Basic(b, c), Basic(a, Basic(f)))
    assert subs(mapping)(expr) == result


def test_subs():
    assert OperationsOnlyMatrix([[1, x], [x, 4]]).subs(x, 5) == Matrix([[1, 5], [5, 4]])
    assert OperationsOnlyMatrix([[x, 2], [x + y, 4]]).subs([[x, -1], [y, -2]]) == \
           Matrix([[-1, 2], [-3, 4]])
    assert OperationsOnlyMatrix([[x, 2], [x + y, 4]]).subs([(x, -1), (y, -2)]) == \
           Matrix([[-1, 2], [-3, 4]])
    assert OperationsOnlyMatrix([[x, 2], [x + y, 4]]).subs({x: -1, y: -2}) == \
           Matrix([[-1, 2], [-3, 4]])
    assert OperationsOnlyMatrix([[x*y]]).subs({x: y - 1, y: x - 1}, simultaneous=True) == \
           Matrix([[(x - 1)*(y - 1)]])


def test_subs():
    A = ImmutableMatrix([[1, 2], [3, 4]])
    B = ImmutableMatrix([[1, 2], [x, 4]])
    C = ImmutableMatrix([[-x, x*y], [-(x + y), y**2]])
    assert B.subs(x, 3) == A
    assert (x*B).subs(x, 3) == 3*A
    assert (x*eye(2) + B).subs(x, 3) == 3*eye(2) + A
    assert C.subs([[x, -1], [y, -2]]) == A
    assert C.subs([(x, -1), (y, -2)]) == A
    assert C.subs({x: -1, y: -2}) == A
    assert C.subs({x: y - 1, y: x - 1}, simultaneous=True) == \
        ImmutableMatrix([[1 - y, (x - 1)*(y - 1)], [2 - x - y, (x - 1)**2]])


def test_subs():
    assert Matrix([[1, x], [x, 4]]).subs(x, 5) == Matrix([[1, 5], [5, 4]])
    assert Matrix([[x, 2], [x + y, 4]]).subs([[x, -1], [y, -2]]) == \
        Matrix([[-1, 2], [-3, 4]])
    assert Matrix([[x, 2], [x + y, 4]]).subs([(x, -1), (y, -2)]) == \
        Matrix([[-1, 2], [-3, 4]])
    assert Matrix([[x, 2], [x + y, 4]]).subs({x: -1, y: -2}) == \
        Matrix([[-1, 2], [-3, 4]])
    assert Matrix([x*y]).subs({x: y - 1, y: x - 1}, simultaneous=True) == \
        Matrix([(x - 1)*(y - 1)])

    for cls in classes:
        assert Matrix([[2, 0], [0, 2]]) == cls.eye(2).subs(1, 2)


def test_subs():
    assert Matrix([[1, x], [x, 4]]).subs(x, 5) == Matrix([[1, 5], [5, 4]])
    assert Matrix([[x, 2], [x + y, 4]]).subs([[x, -1], [y, -2]]) == \
           Matrix([[-1, 2], [-3, 4]])
    assert Matrix([[x, 2], [x + y, 4]]).subs([(x, -1), (y, -2)]) == \
           Matrix([[-1, 2], [-3, 4]])
    assert Matrix([[x, 2], [x + y, 4]]).subs({x: -1, y: -2}) == \
           Matrix([[-1, 2], [-3, 4]])
    assert Matrix([[x*y]]).subs({x: y - 1, y: x - 1}, simultaneous=True) == \
           Matrix([[(x - 1)*(y - 1)]])


def test_subs():
    assert (A & B).subs(A, True) == B
    assert (A & B).subs(A, False) is false
    assert (A & B).subs(B, True) == A
    assert (A & B).subs(B, False) is false
    assert (A & B).subs({A: True, B: True}) is true
    assert (A | B).subs(A, True) is true
    assert (A | B).subs(A, False) == B
    assert (A | B).subs(B, True) is true
    assert (A | B).subs(B, False) == A
    assert (A | B).subs({A: True, B: True}) is true


def test_subs():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    p = Point(x, 2)
    q = Point(1, 1)
    r = Point(3, 4)
    for o in [p,
              Segment(p, q),
              Ray(p, q),
              Line(p, q),
              Triangle(p, q, r),
              RegularPolygon(p, 3, 6),
              Polygon(p, q, r, Point(5, 4)),
              Circle(p, 3),
              Ellipse(p, 3, 4)]:
        assert 'y' in str(o.subs(x, y))
    assert p.subs({x: 1}) == Point(1, 2)
    assert Point(1, 2).subs(Point(1, 2), Point(3, 4)) == Point(3, 4)
    assert Point(1, 2).subs((1, 2), Point(3, 4)) == Point(3, 4)
    assert Point(1, 2).subs(Point(1, 2), Point(3, 4)) == Point(3, 4)
    assert Point(1, 2).subs({(1, 2)}) == Point(2, 2)
    raises(ValueError, lambda: Point(1, 2).subs(1))
    raises(TypeError, lambda: Point(1, 1).subs((Point(1, 1), Point(1,
           2)), 1, 2))


def test_subs():
    assert s1.subs(s1, s2) == s2
    assert v1.subs(v1, v2) == v2
    assert f1.subs(f1, f2) == f2
    assert (x*f(s1) + y).subs(s1, s2) == x*f(s2) + y
    assert (f(s1)*v1).subs(v1, v2) == f(s1)*v2
    assert (y*f(s1)*f1).subs(f1, f2) == y*f(s1)*f2


def test_subs():
    assert b21.subs(b2, b1) == Basic(b1, b1)
    assert b21.subs(b2, b21) == Basic(b21, b1)
    assert b3.subs(b2, b1) == b2

    assert b21.subs([(b2, b1), (b1, b2)]) == Basic(b2, b2)

    assert b21.subs({b1: b2, b2: b1}) == Basic(b2, b2)
    assert b21.subs(collections.ChainMap({b1: b2}, {b2: b1})) == Basic(b2, b2)
    assert b21.subs(collections.OrderedDict([(b2, b1), (b1, b2)])) == Basic(b2, b2)

    raises(ValueError, lambda: b21.subs('bad arg'))
    raises(TypeError, lambda: b21.subs(b1, b2, b3))
    # dict(b1=foo) creates a string 'b1' but leaves foo unchanged; subs
    # will convert the first to a symbol but will raise an error if foo
    # cannot be sympified; sympification is strict if foo is not string
    raises(TypeError, lambda: b21.subs(b1='bad arg'))

    assert Symbol("text").subs({"text": b1}) == b1
    assert Symbol("s").subs({"s": 1}) == 1


def test_subs():
    assert NS('besseli(-x, y) - besseli(x, y)', subs={x: 3.5, y: 20.0}) == \
        '-4.92535585957223e-10'
    assert NS('Piecewise((x, x>0)) + Piecewise((1-x, x>0))', subs={x: 0.1}) == \
        '1.00000000000000'
    raises(TypeError, lambda: x.evalf(subs=(x, 1)))


def test_subs():
    assert (x*y*A).subs(x*y, z) == A*z
    assert (x*A*B).subs(x*A, C) == C*B
    assert (x*A*x*x).subs(x**2*A, C) == x*C
    assert (x*A*x*B).subs(x**2*A, C) == C*B
    assert (A**2*B**2).subs(A*B**2, C) == A*C
    assert (A*A*A + A*B*A).subs(A*A*A, C) == C + A*B*A


def test_subs():
    n3 = Rational(3)
    e = x
    e = e.subs(x, n3)
    assert e == Rational(3)

    e = 2*x
    assert e == 2*x
    e = e.subs(x, n3)
    assert e == Rational(6)

