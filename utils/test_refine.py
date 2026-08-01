
def test_refine():
    m0 = OperationsOnlyMatrix([[Abs(x)**2, sqrt(x**2)],
                 [sqrt(x**2)*Abs(y)**2, sqrt(y**2)*Abs(x)**2]])
    m1 = m0.refine(Q.real(x) & Q.real(y))
    assert m1 == Matrix([[x**2, Abs(x)], [y**2*Abs(x), x**2*Abs(y)]])

    m1 = m0.refine(Q.positive(x) & Q.positive(y))
    assert m1 == Matrix([[x**2, x], [x*y**2, x**2*y]])

    m1 = m0.refine(Q.negative(x) & Q.negative(y))
    assert m1 == Matrix([[x**2, -x], [-x*y**2, -x**2*y]])


def test_refine():
    m0 = Matrix([[Abs(x)**2, sqrt(x**2)],
                [sqrt(x**2)*Abs(y)**2, sqrt(y**2)*Abs(x)**2]])
    m1 = m0.refine(Q.real(x) & Q.real(y))
    assert m1 == Matrix([[x**2, Abs(x)], [y**2*Abs(x), x**2*Abs(y)]])

    m1 = m0.refine(Q.positive(x) & Q.positive(y))
    assert m1 == Matrix([[x**2, x], [x*y**2, x**2*y]])

    m1 = m0.refine(Q.negative(x) & Q.negative(y))
    assert m1 == Matrix([[x**2, -x], [-x*y**2, -x**2*y]])


def test_refine():
    m0 = Matrix([[Abs(x)**2, sqrt(x**2)],
                [sqrt(x**2)*Abs(y)**2, sqrt(y**2)*Abs(x)**2]])
    m1 = m0.refine(Q.real(x) & Q.real(y))
    assert m1 == Matrix([[x**2, Abs(x)], [y**2*Abs(x), x**2*Abs(y)]])

    m1 = m0.refine(Q.positive(x) & Q.positive(y))
    assert m1 == Matrix([[x**2, x], [x*y**2, x**2*y]])

    m1 = m0.refine(Q.negative(x) & Q.negative(y))
    assert m1 == Matrix([[x**2, -x], [-x*y**2, -x**2*y]])


def test_refine():
    assert refine(det(A), Q.orthogonal(A)) == 1
    assert refine(det(A), Q.singular(A)) == 0
    assert refine(det(A), Q.unit_triangular(A)) == 1
    assert refine(det(A), Q.normal(A)) == det(A)


def test_refine():
    assert refine(C.I, Q.orthogonal(C)) == C.T


def test_refine():
    assert refine(C*C.T*D, Q.orthogonal(C)).doit() == D

    kC = k*C
    assert refine(kC*C.T, Q.orthogonal(C)).doit() == k*Identity(n)
    assert refine(kC* kC.T, Q.orthogonal(C)).doit() == (k**2)*Identity(n)


def test_refine():
    assert refine(C.T, Q.symmetric(C)) == C


def test_refine():
    # relational
    assert not refine(x < 0, ~(x < 0))
    assert refine(x < 0, (x < 0))
    assert refine(x < 0, (0 > x)) is S.true
    assert refine(x < 0, (y < 0)) == (x < 0)
    assert not refine(x <= 0, ~(x <= 0))
    assert refine(x <= 0, (x <= 0))
    assert refine(x <= 0, (0 >= x)) is S.true
    assert refine(x <= 0, (y <= 0)) == (x <= 0)
    assert not refine(x > 0, ~(x > 0))
    assert refine(x > 0, (x > 0))
    assert refine(x > 0, (0 < x)) is S.true
    assert refine(x > 0, (y > 0)) == (x > 0)
    assert not refine(x >= 0, ~(x >= 0))
    assert refine(x >= 0, (x >= 0))
    assert refine(x >= 0, (0 <= x)) is S.true
    assert refine(x >= 0, (y >= 0)) == (x >= 0)
    assert not refine(Eq(x, 0), ~(Eq(x, 0)))
    assert refine(Eq(x, 0), (Eq(x, 0)))
    assert refine(Eq(x, 0), (Eq(0, x))) is S.true
    assert refine(Eq(x, 0), (Eq(y, 0))) == Eq(x, 0)
    assert not refine(Ne(x, 0), ~(Ne(x, 0)))
    assert refine(Ne(x, 0), (Ne(0, x))) is S.true
    assert refine(Ne(x, 0), (Ne(x, 0)))
    assert refine(Ne(x, 0), (Ne(y, 0))) == (Ne(x, 0))

    # boolean functions
    assert refine(And(x > 0, y > 0), (x > 0)) == (y > 0)
    assert refine(And(x > 0, y > 0), (x > 0) & (y > 0)) is S.true

    # predicates
    assert refine(Q.positive(x), Q.positive(x)) is S.true
    assert refine(Q.positive(x), Q.negative(x)) is S.false
    assert refine(Q.positive(x), Q.real(x)) == Q.positive(x)

