
def test_anticommutator():
    ac = AComm(A, B)
    assert isinstance(ac, AComm)
    assert ac.is_commutative is False
    assert ac.subs(A, C) == AComm(C, B)


def test_anticommutator():
    A = Operator('A')
    B = Operator('B')
    ac = AntiCommutator(A, B)
    ac_tall = AntiCommutator(A**2, B)
    assert str(ac) == '{A,B}'
    assert pretty(ac) == '{A,B}'
    assert upretty(ac) == '{A,B}'
    assert latex(ac) == r'\left\{A,B\right\}'
    sT(ac, "AntiCommutator(Operator(Symbol('A')),Operator(Symbol('B')))")
    assert str(ac_tall) == '{A**2,B}'
    ascii_str = \
"""\
/ 2  \\\n\
<A ,B>\n\
\\    /\
"""
    ucode_str = \
"""\
⎧ 2  ⎫\n\
⎨A ,B⎬\n\
⎩    ⎭\
"""
    assert pretty(ac_tall) == ascii_str
    assert upretty(ac_tall) == ucode_str
    assert latex(ac_tall) == r'\left\{A^{2},B\right\}'
    sT(ac_tall, "AntiCommutator(Pow(Operator(Symbol('A')), Integer(2)),Operator(Symbol('B')))")


def test_anticommutator():
    assert qapply(AntiCommutator(Jz, Foo('F'))*po) == 2*hbar*po
    assert qapply(AntiCommutator(Foo('F'), Jz)*po) == 2*hbar*po

