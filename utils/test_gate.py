
def test_gate():
    """Test a basic gate."""
    h = HadamardGate(1)
    assert h.min_qubits == 2
    assert h.nqubits == 1

    i0 = Wild('i0')
    i1 = Wild('i1')
    h0_w1 = HadamardGate(i0)
    h0_w2 = HadamardGate(i0)
    h1_w1 = HadamardGate(i1)

    assert h0_w1 == h0_w2
    assert h0_w1 != h1_w1
    assert h1_w1 != h0_w2

    cnot_10_w1 = CNOT(i1, i0)
    cnot_10_w2 = CNOT(i1, i0)
    cnot_01_w1 = CNOT(i0, i1)

    assert cnot_10_w1 == cnot_10_w2
    assert cnot_10_w1 != cnot_01_w1
    assert cnot_10_w2 != cnot_01_w1


def test_gate():
    a, b, c, d = symbols('a,b,c,d')
    uMat = Matrix([[a, b], [c, d]])
    q = Qubit(1, 0, 1, 0, 1)
    g1 = IdentityGate(2)
    g2 = CGate((3, 0), XGate(1))
    g3 = CNotGate(1, 0)
    g4 = UGate((0,), uMat)
    assert str(g1) == '1(2)'
    assert pretty(g1) == '1 \n 2'
    assert upretty(g1) == '1 \n 2'
    assert latex(g1) == r'1_{2}'
    sT(g1, "IdentityGate(Integer(2))")
    assert str(g1*q) == '1(2)*|10101>'
    ascii_str = \
"""\
1 *|10101>\n\
 2        \
"""
    ucode_str = \
"""\
1 ⋅❘10101⟩\n\
 2        \
"""
    assert pretty(g1*q) == ascii_str
    assert upretty(g1*q) == ucode_str
    assert latex(g1*q) == r'1_{2} {\left|10101\right\rangle }'
    sT(g1*q, "Mul(IdentityGate(Integer(2)), Qubit(Integer(1),Integer(0),Integer(1),Integer(0),Integer(1)))")
    assert str(g2) == 'C((3,0),X(1))'
    ascii_str = \
"""\
C   /X \\\n\
 3,0\\ 1/\
"""
    ucode_str = \
"""\
C   ⎛X ⎞\n\
 3,0⎝ 1⎠\
"""
    assert pretty(g2) == ascii_str
    assert upretty(g2) == ucode_str
    assert latex(g2) == r'C_{3,0}{\left(X_{1}\right)}'
    sT(g2, "CGate(Tuple(Integer(3), Integer(0)),XGate(Integer(1)))")
    assert str(g3) == 'CNOT(1,0)'
    ascii_str = \
"""\
CNOT   \n\
    1,0\
"""
    ucode_str = \
"""\
CNOT   \n\
    1,0\
"""
    assert pretty(g3) == ascii_str
    assert upretty(g3) == ucode_str
    assert latex(g3) == r'\text{CNOT}_{1,0}'
    sT(g3, "CNotGate(Integer(1),Integer(0))")
    ascii_str = \
"""\
U \n\
 0\
"""
    ucode_str = \
"""\
U \n\
 0\
"""
    assert str(g4) == \
"""\
U((0,),Matrix([\n\
[a, b],\n\
[c, d]]))\
"""
    assert pretty(g4) == ascii_str
    assert upretty(g4) == ucode_str
    assert latex(g4) == r'U_{0}'
    sT(g4, "UGate(Tuple(Integer(0)),ImmutableDenseMatrix([[Symbol('a'), Symbol('b')], [Symbol('c'), Symbol('d')]]))")

