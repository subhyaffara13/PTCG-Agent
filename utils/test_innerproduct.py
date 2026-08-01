
def test_innerproduct():
    k = Ket('k')
    b = Bra('b')
    ip = InnerProduct(b, k)
    assert isinstance(ip, InnerProduct)
    assert ip.bra == b
    assert ip.ket == k
    assert b*k == InnerProduct(b, k)
    assert k*(b*k)*b == k*InnerProduct(b, k)*b
    assert InnerProduct(b, k).subs(b, Dagger(k)) == Dagger(k)*k


def test_innerproduct():
    x = symbols('x')
    ip1 = InnerProduct(Bra(), Ket())
    ip2 = InnerProduct(TimeDepBra(), TimeDepKet())
    ip3 = InnerProduct(JzBra(1, 1), JzKet(1, 1))
    ip4 = InnerProduct(JzBraCoupled(1, 1, (1, 1)), JzKetCoupled(1, 1, (1, 1)))
    ip_tall1 = InnerProduct(Bra(x/2), Ket(x/2))
    ip_tall2 = InnerProduct(Bra(x), Ket(x/2))
    ip_tall3 = InnerProduct(Bra(x/2), Ket(x))
    assert str(ip1) == '<psi|psi>'
    assert pretty(ip1) == '<psi|psi>'
    assert upretty(ip1) == '⟨ψ❘ψ⟩'
    assert latex(
        ip1) == r'\left\langle \psi \right. {\left|\psi\right\rangle }'
    sT(ip1, "InnerProduct(Bra(Symbol('psi')),Ket(Symbol('psi')))")
    assert str(ip2) == '<psi;t|psi;t>'
    assert pretty(ip2) == '<psi;t|psi;t>'
    assert upretty(ip2) == '⟨ψ;t❘ψ;t⟩'
    assert latex(ip2) == \
        r'\left\langle \psi;t \right. {\left|\psi;t\right\rangle }'
    sT(ip2, "InnerProduct(TimeDepBra(Symbol('psi'),Symbol('t')),TimeDepKet(Symbol('psi'),Symbol('t')))")
    assert str(ip3) == "<1,1|1,1>"
    assert pretty(ip3) == '<1,1|1,1>'
    assert upretty(ip3) == '⟨1,1❘1,1⟩'
    assert latex(ip3) == r'\left\langle 1,1 \right. {\left|1,1\right\rangle }'
    sT(ip3, "InnerProduct(JzBra(Integer(1),Integer(1)),JzKet(Integer(1),Integer(1)))")
    assert str(ip4) == "<1,1,j1=1,j2=1|1,1,j1=1,j2=1>"
    assert pretty(ip4) == '<1,1,j1=1,j2=1|1,1,j1=1,j2=1>'
    assert upretty(ip4) == '⟨1,1,j₁=1,j₂=1❘1,1,j₁=1,j₂=1⟩'
    assert latex(ip4) == \
        r'\left\langle 1,1,j_{1}=1,j_{2}=1 \right. {\left|1,1,j_{1}=1,j_{2}=1\right\rangle }'
    sT(ip4, "InnerProduct(JzBraCoupled(Integer(1),Integer(1),Tuple(Integer(1), Integer(1)),Tuple(Tuple(Integer(1), Integer(2), Integer(1)))),JzKetCoupled(Integer(1),Integer(1),Tuple(Integer(1), Integer(1)),Tuple(Tuple(Integer(1), Integer(2), Integer(1)))))")
    assert str(ip_tall1) == '<x/2|x/2>'
    ascii_str = \
"""\
 / | \\ \n\
/ x|x \\\n\
\\ -|- /\n\
 \\2|2/ \
"""
    ucode_str = \
"""\
 ╱ │ ╲ \n\
╱ x│x ╲\n\
╲ ─│─ ╱\n\
 ╲2│2╱ \
"""
    assert pretty(ip_tall1) == ascii_str
    assert upretty(ip_tall1) == ucode_str
    assert latex(ip_tall1) == \
        r'\left\langle \frac{x}{2} \right. {\left|\frac{x}{2}\right\rangle }'
    sT(ip_tall1, "InnerProduct(Bra(Mul(Rational(1, 2), Symbol('x'))),Ket(Mul(Rational(1, 2), Symbol('x'))))")
    assert str(ip_tall2) == '<x|x/2>'
    ascii_str = \
"""\
 / | \\ \n\
/  |x \\\n\
\\ x|- /\n\
 \\ |2/ \
"""
    ucode_str = \
"""\
 ╱ │ ╲ \n\
╱  │x ╲\n\
╲ x│─ ╱\n\
 ╲ │2╱ \
"""
    assert pretty(ip_tall2) == ascii_str
    assert upretty(ip_tall2) == ucode_str
    assert latex(ip_tall2) == \
        r'\left\langle x \right. {\left|\frac{x}{2}\right\rangle }'
    sT(ip_tall2,
       "InnerProduct(Bra(Symbol('x')),Ket(Mul(Rational(1, 2), Symbol('x'))))")
    assert str(ip_tall3) == '<x/2|x>'
    ascii_str = \
"""\
 / | \\ \n\
/ x|  \\\n\
\\ -|x /\n\
 \\2| / \
"""
    ucode_str = \
"""\
 ╱ │ ╲ \n\
╱ x│  ╲\n\
╲ ─│x ╱\n\
 ╲2│ ╱ \
"""
    assert pretty(ip_tall3) == ascii_str
    assert upretty(ip_tall3) == ucode_str
    assert latex(ip_tall3) == \
        r'\left\langle \frac{x}{2} \right. {\left|x\right\rangle }'
    sT(ip_tall3,
       "InnerProduct(Bra(Mul(Rational(1, 2), Symbol('x'))),Ket(Symbol('x')))")


def test_innerproduct():
    assert qapply(po.dual*Jz*po, ip_doit=False) == hbar*(po.dual*po)
    assert qapply(po.dual*Jz*po) == hbar


def test_innerproduct():
    assert InnerProduct(JzBra(1, 1), JzKet(1, 1)).doit() == 1
    assert InnerProduct(
        JzBra(S.Half, S.Half), JzKet(S.Half, Rational(-1, 2))).doit() == 0
    assert InnerProduct(JzBra(j, m), JzKet(j, m)).doit() == 1
    assert InnerProduct(JzBra(1, 0), JyKet(1, 1)).doit() == I/sqrt(2)
    assert InnerProduct(
        JxBra(S.Half, S.Half), JzKet(S.Half, S.Half)).doit() == -sqrt(2)/2
    assert InnerProduct(JyBra(1, 1), JzKet(1, 1)).doit() == S.Half
    assert InnerProduct(JxBra(1, -1), JyKet(1, 1)).doit() == 0

