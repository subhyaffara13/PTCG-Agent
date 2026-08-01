
def test_operator():
    i, j = symbols('i,j')
    o = BosonicOperator(i)
    assert o.state == i
    assert o.is_symbolic
    o = BosonicOperator(1)
    assert o.state == 1
    assert not o.is_symbolic


def test_operator():
    A = Operator('A')
    B = Operator('B')
    C = Operator('C')

    assert isinstance(A, Operator)
    assert isinstance(A, QExpr)

    assert A.label == (Symbol('A'),)
    assert A.is_commutative is False
    assert A.hilbert_space == HilbertSpace()

    assert A*B != B*A

    assert (A*(B + C)).expand() == A*B + A*C
    assert ((A + B)**2).expand() == A**2 + A*B + B*A + B**2

    assert t_op.label[0] == Symbol(t_op.default_args()[0])

    assert Operator() == Operator("O")
    with warns_deprecated_sympy():
        assert A*IdentityOperator() == A


def test_operator():
    a = Operator('A')
    b = Operator('B', Symbol('t'), S.Half)
    inv = a.inv()
    f = Function('f')
    x = symbols('x')
    d = DifferentialOperator(Derivative(f(x), x), f(x))
    op = OuterProduct(Ket(), Bra())
    assert str(a) == 'A'
    assert pretty(a) == 'A'
    assert upretty(a) == 'A'
    assert latex(a) == 'A'
    sT(a, "Operator(Symbol('A'))")
    assert str(inv) == 'A**(-1)'
    ascii_str = \
"""\
 -1\n\
A  \
"""
    ucode_str = \
"""\
 -1\n\
A  \
"""
    assert pretty(inv) == ascii_str
    assert upretty(inv) == ucode_str
    assert latex(inv) == r'A^{-1}'
    sT(inv, "Pow(Operator(Symbol('A')), Integer(-1))")
    assert str(d) == 'DifferentialOperator(Derivative(f(x), x),f(x))'
    ascii_str = \
"""\
                    /d            \\\n\
DifferentialOperator|--(f(x)),f(x)|\n\
                    \\dx           /\
"""
    ucode_str = \
"""\
                    ⎛d            ⎞\n\
DifferentialOperator⎜──(f(x)),f(x)⎟\n\
                    ⎝dx           ⎠\
"""
    assert pretty(d) == ascii_str
    assert upretty(d) == ucode_str
    assert latex(d) == \
        r'DifferentialOperator\left(\frac{d}{d x} f{\left(x \right)},f{\left(x \right)}\right)'
    sT(d, "DifferentialOperator(Derivative(Function('f')(Symbol('x')), Tuple(Symbol('x'), Integer(1))),Function('f')(Symbol('x')))")
    assert str(b) == 'Operator(B,t,1/2)'
    assert pretty(b) == 'Operator(B,t,1/2)'
    assert upretty(b) == 'Operator(B,t,1/2)'
    assert latex(b) == r'Operator\left(B,t,\frac{1}{2}\right)'
    sT(b, "Operator(Symbol('B'),Symbol('t'),Rational(1, 2))")
    assert str(op) == '|psi><psi|'
    assert pretty(op) == '|psi><psi|'
    assert upretty(op) == '❘ψ⟩⟨ψ❘'
    assert latex(op) == r'{\left|\psi\right\rangle }{\left\langle \psi\right|}'
    sT(op, "OuterProduct(Ket(Symbol('psi')),Bra(Symbol('psi')))")

