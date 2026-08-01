
def test_conjugate_transpose():
    A, B = symbols("A B", commutative=False)

    x = Symbol("x", complex=True)
    p = Integral(A*B, (x,))
    assert p.adjoint().doit() == p.doit().adjoint()
    assert p.conjugate().doit() == p.doit().conjugate()
    assert p.transpose().doit() == p.doit().transpose()

    x = Symbol("x", real=True)
    p = Integral(A*B, (x,))
    assert p.adjoint().doit() == p.doit().adjoint()
    assert p.conjugate().doit() == p.doit().conjugate()
    assert p.transpose().doit() == p.doit().transpose()


def test_conjugate_transpose():
    x = Symbol('x', commutative=False)
    assert conjugate(transpose(x)) == adjoint(x)
    assert transpose(conjugate(x)) == adjoint(x)
    assert adjoint(transpose(x)) == conjugate(x)
    assert transpose(adjoint(x)) == conjugate(x)
    assert adjoint(conjugate(x)) == transpose(x)
    assert conjugate(adjoint(x)) == transpose(x)

    x = Symbol('x')
    assert conjugate(x) == adjoint(x)
    assert transpose(x) == x


def test_conjugate_transpose():
    A, B = symbols("A B", commutative=False)
    p = Piecewise((A*B**2, x > 0), (A**2*B, True))
    assert p.adjoint() == \
        Piecewise((adjoint(A*B**2), x > 0), (adjoint(A**2*B), True))
    assert p.conjugate() == \
        Piecewise((conjugate(A*B**2), x > 0), (conjugate(A**2*B), True))
    assert p.transpose() == \
        Piecewise((transpose(A*B**2), x > 0), (transpose(A**2*B), True))


def test_conjugate_transpose():
    p = Product(x**k, (k, 1, 3))
    assert p.adjoint().doit() == p.doit().adjoint()
    assert p.conjugate().doit() == p.doit().conjugate()
    assert p.transpose().doit() == p.doit().transpose()

    A, B = symbols("A B", commutative=False)
    p = Product(A*B**k, (k, 1, 3))
    assert p.adjoint().doit() == p.doit().adjoint()
    assert p.conjugate().doit() == p.doit().conjugate()
    assert p.transpose().doit() == p.doit().transpose()

    p = Product(B**k*A, (k, 1, 3))
    assert p.adjoint().doit() == p.doit().adjoint()
    assert p.conjugate().doit() == p.doit().conjugate()
    assert p.transpose().doit() == p.doit().transpose()


def test_conjugate_transpose():
    A, B = symbols("A B", commutative=False)
    p = Sum(A*B**n, (n, 1, 3))
    assert p.adjoint().doit() == p.doit().adjoint()
    assert p.conjugate().doit() == p.doit().conjugate()
    assert p.transpose().doit() == p.doit().transpose()

    p = Sum(B**n*A, (n, 1, 3))
    assert p.adjoint().doit() == p.doit().adjoint()
    assert p.conjugate().doit() == p.doit().conjugate()
    assert p.transpose().doit() == p.doit().transpose()

