
def test_latex_Piecewise():
    p = Piecewise((x, x < 1), (x**2, True))
    assert latex(p) == r"\begin{cases} x & \text{for}\: x < 1 \\x^{2} &" \
                       r" \text{otherwise} \end{cases}"
    assert latex(p, itex=True) == \
        r"\begin{cases} x & \text{for}\: x \lt 1 \\x^{2} &" \
        r" \text{otherwise} \end{cases}"
    p = Piecewise((x, x < 0), (0, x >= 0))
    assert latex(p) == r'\begin{cases} x & \text{for}\: x < 0 \\0 &' \
                       r' \text{otherwise} \end{cases}'
    A, B = symbols("A B", commutative=False)
    p = Piecewise((A**2, Eq(A, B)), (A*B, True))
    s = r"\begin{cases} A^{2} & \text{for}\: A = B \\A B & \text{otherwise} \end{cases}"
    assert latex(p) == s
    assert latex(A*p) == r"A \left(%s\right)" % s
    assert latex(p*A) == r"\left(%s\right) A" % s
    assert latex(Piecewise((x, x < 1), (x**2, x < 2))) == \
        r'\begin{cases} x & ' \
        r'\text{for}\: x < 1 \\x^{2} & \text{for}\: x < 2 \end{cases}'

