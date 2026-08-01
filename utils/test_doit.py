
def test_doit():
    f = Integral(2 * x, x)
    l = Limit(f, x, oo)
    assert l.doit() is oo


def test_doit():
    assert Wigner3j(S.Half, Rational(-1, 2), S.Half, S.Half, 0, 0).doit() == -sqrt(2)/2
    assert Wigner3j(1/2,1/2,1/2,1/2,1/2,1/2).doit() == 0
    assert Wigner3j(9/2,9/2,9/2,9/2,9/2,9/2).doit() ==  0
    assert Wigner6j(1, 2, 3, 2, 1, 2).doit() == sqrt(21)/105
    assert Wigner6j(3, 1, 2, 2, 2, 1).doit() == sqrt(21) / 105
    assert Wigner9j(
        2, 1, 1, Rational(3, 2), S.Half, 1, S.Half, S.Half, 0).doit() == sqrt(2)/12
    assert CG(S.Half, S.Half, S.Half, Rational(-1, 2), 1, 0).doit() == sqrt(2)/2
    # J minus M is not integer
    assert Wigner3j(1, -1, S.Half, S.Half, 1, S.Half).doit() == 0
    assert CG(4, -1, S.Half, S.Half, 4, Rational(-1, 2)).doit() == 0


def test_doit():

    x, y = symbols('x y')
    A, B, C, D, E, F = symbols('A B C D E F', commutative=False)
    d = Density([XKet(), 0.5], [PxKet(), 0.5])
    assert (0.5*(PxKet()*Dagger(PxKet())) +
            0.5*(XKet()*Dagger(XKet()))) == d.doit()

    # check for kets with expr in them
    d_with_sym = Density([XKet(x*y), 0.5], [PxKet(x*y), 0.5])
    assert (0.5*(PxKet(x*y)*Dagger(PxKet(x*y))) +
            0.5*(XKet(x*y)*Dagger(XKet(x*y)))) == d_with_sym.doit()

    d = Density([(A + B)*C, 1.0])
    assert d.doit() == (1.0*A*C*Dagger(C)*Dagger(A) +
                        1.0*A*C*Dagger(C)*Dagger(B) +
                        1.0*B*C*Dagger(C)*Dagger(A) +
                        1.0*B*C*Dagger(C)*Dagger(B))

    #  With TensorProducts as args
    # Density with simple tensor products as args
    t = TensorProduct(A, B, C)
    d = Density([t, 1.0])
    assert d.doit() == \
        1.0 * TensorProduct(A*Dagger(A), B*Dagger(B), C*Dagger(C))

    # Density with multiple Tensorproducts as states
    t2 = TensorProduct(A, B)
    t3 = TensorProduct(C, D)

    d = Density([t2, 0.5], [t3, 0.5])
    assert d.doit() == (0.5 * TensorProduct(A*Dagger(A), B*Dagger(B)) +
                        0.5 * TensorProduct(C*Dagger(C), D*Dagger(D)))

    #Density with mixed states
    d = Density([t2 + t3, 1.0])
    assert d.doit() == (1.0 * TensorProduct(A*Dagger(A), B*Dagger(B)) +
                        1.0 * TensorProduct(A*Dagger(C), B*Dagger(D)) +
                        1.0 * TensorProduct(C*Dagger(A), D*Dagger(B)) +
                        1.0 * TensorProduct(C*Dagger(C), D*Dagger(D)))

    #Density operators with spin states
    tp1 = TensorProduct(JzKet(1, 1), JzKet(1, -1))
    d = Density([tp1, 1])

    # full trace
    t = Tr(d)
    assert t.doit() == 1

    #Partial trace on density operators with spin states
    t = Tr(d, [0])
    assert t.doit() == JzKet(1, -1) * Dagger(JzKet(1, -1))
    t = Tr(d, [1])
    assert t.doit() == JzKet(1, 1) * Dagger(JzKet(1, 1))

    # with another spin state
    tp2 = TensorProduct(JzKet(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2)))
    d = Density([tp2, 1])

    #full trace
    t = Tr(d)
    assert t.doit() == 1

    #Partial trace on density operators with spin states
    t = Tr(d, [0])
    assert t.doit() == JzKet(S.Half, Rational(-1, 2)) * Dagger(JzKet(S.Half, Rational(-1, 2)))
    t = Tr(d, [1])
    assert t.doit() == JzKet(S.Half, S.Half) * Dagger(JzKet(S.Half, S.Half))


def test_doit():
    f = FooKet('foo')
    b = BarBra('bar')
    assert InnerProduct(b, f).doit() == I
    assert InnerProduct(Dagger(f), Dagger(b)).doit() == -I
    assert InnerProduct(Dagger(f), f).doit() == Integer(1)


def test_doit():
    a = OperationsOnlyMatrix([[Add(x, x, evaluate=False)]])
    assert a[0] != 2*x
    assert a.doit() == Matrix([[2*x]])


def test_doit():
    a = Matrix([[Add(x,x, evaluate=False)]])
    assert a[0] != 2*x
    assert a.doit() == Matrix([[2*x]])


def test_doit():
    a = Matrix([[Add(x, x, evaluate=False)]])
    assert a[0] != 2*x
    assert a.doit() == Matrix([[2*x]])


def test_doit():
    assert MatMul(C, 2, D).args == (C, 2, D)
    assert MatMul(C, 2, D).doit().args == (2, C, D)
    assert MatMul(C, Transpose(D*C)).args == (C, Transpose(D*C))
    assert MatMul(C, Transpose(D*C)).doit(deep=True).args == (C, C.T, D.T)


def test_doit():
    p1 = Piecewise((x, x < 1), (x**2, -1 <= x), (x, 3 < x))
    p2 = Piecewise((x, x < 1), (Integral(2 * x), -1 <= x), (x, 3 < x))
    assert p2.doit() == p1
    assert p2.doit(deep=False) == p2
    # issue 17165
    p1 = Sum(y**x, (x, -1, oo)).doit()
    assert p1.doit() == p1


def test_doit():
    assert b21.doit() == b21
    assert b21.doit(deep=False) == b21


def test_doit():
    a = Integral(x**2, x)

    assert isinstance(a.doit(), Integral) is False

    assert isinstance(a.doit(integrals=True), Integral) is False
    assert isinstance(a.doit(integrals=False), Integral) is True

    assert (2*Integral(x, x)).doit() == x**2


def test_doit():
    n = Symbol('n', integer=True)
    f = Sum(2 * n * x, (n, 1, 3))
    d = Derivative(f, x)
    assert d.doit() == 12
    assert d.doit(deep=False) == Sum(2*n, (n, 1, 3))


def test_doit():
    from sympy.core.symbol import Symbol
    p = Symbol('p', positive=True)
    n = Symbol('n', negative=True)
    np = Symbol('np', nonpositive=True)
    nn = Symbol('nn', nonnegative=True)

    assert Gt(p, 0).doit() is S.true
    assert Gt(p, 1).doit() == Gt(p, 1)
    assert Ge(p, 0).doit() is S.true
    assert Le(p, 0).doit() is S.false
    assert Lt(n, 0).doit() is S.true
    assert Le(np, 0).doit() is S.true
    assert Gt(nn, 0).doit() == Gt(nn, 0)
    assert Lt(nn, 0).doit() is S.false

    assert Eq(x, 0).doit() == Eq(x, 0)

