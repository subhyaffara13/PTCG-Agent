
def test_dagger():
    i, j, n, m = symbols('i,j,n,m')
    assert Dagger(1) == 1
    assert Dagger(1.0) == 1.0
    assert Dagger(2*I) == -2*I
    assert Dagger(S.Half*I/3.0) == I*Rational(-1, 2)/3.0
    assert Dagger(BKet([n])) == BBra([n])
    assert Dagger(B(0)) == Bd(0)
    assert Dagger(Bd(0)) == B(0)
    assert Dagger(B(n)) == Bd(n)
    assert Dagger(Bd(n)) == B(n)
    assert Dagger(B(0) + B(1)) == Bd(0) + Bd(1)
    assert Dagger(n*m) == Dagger(n)*Dagger(m)  # n, m commute
    assert Dagger(B(n)*B(m)) == Bd(m)*Bd(n)
    assert Dagger(B(n)**10) == Dagger(B(n))**10
    assert Dagger('a') == Dagger(Symbol('a'))
    assert Dagger(Dagger('a')) == Symbol('a')
    assert Dagger(exp(2 * I)) == exp(-2 * I)
    assert Dagger(i) == conjugate(i)


def test_dagger():
    x = symbols('x', commutative=False)
    expr = Dagger(x)
    assert str(expr) == 'Dagger(x)'
    ascii_str = \
"""\
 +\n\
x \
"""
    ucode_str = \
"""\
 †\n\
x \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str
    assert latex(expr) == r'x^{\dagger}'
    sT(expr, "Dagger(Symbol('x', commutative=False))")


def test_dagger():
    lhs = Dagger(Qubit(0))*Dagger(H(0))
    rhs = Dagger(Qubit(1))/sqrt(2) + Dagger(Qubit(0))/sqrt(2)
    assert qapply(lhs, dagger=True) == rhs

