
def test_hadamard_power():
    m, n, p = symbols('m, n, p', integer=True)
    A = MatrixSymbol('A', m, n)
    B = MatrixSymbol('B', m, n)

    # Testing printer:
    expr = hadamard_power(A, n)
    ascii_str = \
"""\
 .n\n\
A  \
"""
    ucode_str = \
"""\
 ∘n\n\
A  \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = hadamard_power(A, 1+n)
    ascii_str = \
"""\
 .(n + 1)\n\
A        \
"""
    ucode_str = \
"""\
 ∘(n + 1)\n\
A        \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = hadamard_power(A*B.T, 1+n)
    ascii_str = \
"""\
      .(n + 1)\n\
/   T\\        \n\
\\A*B /        \
"""
    ucode_str = \
"""\
      ∘(n + 1)\n\
⎛   T⎞        \n\
⎝A⋅B ⎠        \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str


def test_hadamard_power():
    m, n, p = symbols('m, n, p', integer=True)
    A = MatrixSymbol('A', m, n)

    assert hadamard_power(A, 1) == A
    assert isinstance(hadamard_power(A, 2), HadamardPower)
    assert hadamard_power(A, n).T == hadamard_power(A.T, n)
    assert hadamard_power(A, n)[0, 0] == A[0, 0]**n
    assert hadamard_power(m, n) == m**n
    raises(ValueError, lambda: hadamard_power(A, A))

