
def test_linsolve():
    x1, x2, x3, x4 = symbols('x1, x2, x3, x4')

    # Test for different input forms

    M = Matrix([[1, 2, 1, 1, 7], [1, 2, 2, -1, 12], [2, 4, 0, 6, 4]])
    system1 = A, B = M[:, :-1], M[:, -1]
    Eqns = [x1 + 2*x2 + x3 + x4 - 7, x1 + 2*x2 + 2*x3 - x4 - 12,
            2*x1 + 4*x2 + 6*x4 - 4]

    sol = FiniteSet((-2*x2 - 3*x4 + 2, x2, 2*x4 + 5, x4))
    assert linsolve(Eqns, (x1, x2, x3, x4)) == sol
    assert linsolve(Eqns, *(x1, x2, x3, x4)) == sol
    assert linsolve(system1, (x1, x2, x3, x4)) == sol
    assert linsolve(system1, *(x1, x2, x3, x4)) == sol
    # issue 9667 - symbols can be Dummy symbols
    x1, x2, x3, x4 = symbols('x:4', cls=Dummy)
    assert linsolve(system1, x1, x2, x3, x4) == FiniteSet(
        (-2*x2 - 3*x4 + 2, x2, 2*x4 + 5, x4))

    # raise ValueError for garbage value
    raises(ValueError, lambda: linsolve(Eqns))
    raises(ValueError, lambda: linsolve(x1))
    raises(ValueError, lambda: linsolve(x1, x2))
    raises(ValueError, lambda: linsolve((A,), x1, x2))
    raises(ValueError, lambda: linsolve(A, B, x1, x2))
    raises(ValueError, lambda: linsolve([x1], x1, x1))
    raises(ValueError, lambda: linsolve([x1], (i for i in (x1, x1))))

    #raise ValueError if equations are non-linear in given variables
    raises(NonlinearError, lambda: linsolve([x + y - 1, x ** 2 + y - 3], [x, y]))
    raises(NonlinearError, lambda: linsolve([cos(x) + y, x + y], [x, y]))
    assert linsolve([x + z - 1, x ** 2 + y - 3], [z, y]) == {(-x + 1, -x**2 + 3)}

    # Fully symbolic test
    A = Matrix([[a, b], [c, d]])
    B = Matrix([[e], [g]])
    system2 = (A, B)
    sol = FiniteSet(((-b*g + d*e)/(a*d - b*c), (a*g - c*e)/(a*d - b*c)))
    assert linsolve(system2, [x, y]) == sol

    # No solution
    A = Matrix([[1, 2, 3], [2, 4, 6], [3, 6, 9]])
    B = Matrix([0, 0, 1])
    assert linsolve((A, B), (x, y, z)) is S.EmptySet

    # Issue #10056
    A, B, J1, J2 = symbols('A B J1 J2')
    Augmatrix = Matrix([
        [2*I*J1, 2*I*J2, -2/J1],
        [-2*I*J2, -2*I*J1, 2/J2],
        [0, 2, 2*I/(J1*J2)],
        [2, 0,  0],
        ])

    assert linsolve(Augmatrix, A, B) == FiniteSet((0, I/(J1*J2)))

    # Issue #10121 - Assignment of free variables
    Augmatrix = Matrix([[0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0]])
    assert linsolve(Augmatrix, a, b, c, d, e) == FiniteSet((a, 0, c, 0, e))
    #raises(IndexError, lambda: linsolve(Augmatrix, a, b, c))

    x0, x1, x2, _x0 = symbols('tau0 tau1 tau2 _tau0')
    assert linsolve(Matrix([[0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, _x0]])
        ) == FiniteSet((x0, 0, x1, _x0, x2))
    x0, x1, x2, _x0 = symbols('tau00 tau01 tau02 tau0')
    assert linsolve(Matrix([[0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, _x0]])
        ) == FiniteSet((x0, 0, x1, _x0, x2))
    x0, x1, x2, _x0 = symbols('tau00 tau01 tau02 tau1')
    assert linsolve(Matrix([[0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 0, _x0]])
        ) == FiniteSet((x0, 0, x1, _x0, x2))
    # symbols can be given as generators
    x0, x2, x4 = symbols('x0, x2, x4')
    assert linsolve(Augmatrix, numbered_symbols('x')
        ) == FiniteSet((x0, 0, x2, 0, x4))
    Augmatrix[-1, -1] = x0
    # use Dummy to avoid clash; the names may clash but the symbols
    # will not
    Augmatrix[-1, -1] = symbols('_x0')
    assert len(linsolve(
        Augmatrix, numbered_symbols('x', cls=Dummy)).free_symbols) == 4

    # Issue #12604
    f = Function('f')
    assert linsolve([f(x) - 5], f(x)) == FiniteSet((5,))

    # Issue #14860
    from sympy.physics.units import meter, newton, kilo
    kN = kilo*newton
    Eqns = [8*kN + x + y, 28*kN*meter + 3*x*meter]
    assert linsolve(Eqns, x, y) == {
            (kilo*newton*Rational(-28, 3), kN*Rational(4, 3))}

    # linsolve does not allow expansion (real or implemented)
    # to remove singularities, but it will cancel linear terms
    assert linsolve([Eq(x, x + y)], [x, y]) == {(x, 0)}
    assert linsolve([Eq(x + x*y, 1 + y)], [x]) == {(1,)}
    assert linsolve([Eq(1 + y, x + x*y)], [x]) == {(1,)}
    raises(NonlinearError, lambda:
        linsolve([Eq(x**2, x**2 + y)], [x, y]))

    # corner cases
    #
    # XXX: The case below should give the same as for [0]
    # assert linsolve([], [x]) == {(x,)}
    assert linsolve([], [x]) is S.EmptySet
    assert linsolve([0], [x]) == {(x,)}
    assert linsolve([x], [x, y]) == {(0, y)}
    assert linsolve([x, 0], [x, y]) == {(0, y)}

