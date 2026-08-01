
def test_matMul():
    A = MatrixSymbol('A', 5, 5)
    B = MatrixSymbol('B', 5, 5)
    x = Symbol('x')
    assert latex(2*A) == r'2 A'
    assert latex(2*x*A) == r'2 x A'
    assert latex(-2*A) == r'- 2 A'
    assert latex(1.5*A) == r'1.5 A'
    assert latex(sqrt(2)*A) == r'\sqrt{2} A'
    assert latex(-sqrt(2)*A) == r'- \sqrt{2} A'
    assert latex(2*sqrt(2)*x*A) == r'2 \sqrt{2} x A'
    assert latex(-2*A*(A + 2*B)) in [r'- 2 A \left(A + 2 B\right)',
                                        r'- 2 A \left(2 B + A\right)']

