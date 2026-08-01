
def test_MatrixSymbol_printing():
    # test cases for issue #14237
    A = MatrixSymbol("A", 3, 3)
    B = MatrixSymbol("B", 3, 3)
    C = MatrixSymbol("C", 3, 3)

    assert latex(-A) == r"- A"
    assert latex(A - A*B - B) == r"A - A B - B"
    assert latex(-A*B - A*B*C - B) == r"- A B - A B C - B"


def test_MatrixSymbol_printing():
    A = MatrixSymbol("A", 3, 3)
    B = MatrixSymbol("B", 3, 3)

    assert str(A - A*B - B) == "A - A*B - B"
    assert str(A*B - (A+B)) == "-A + A*B - B"
    assert str(A**(-1)) == "A**(-1)"
    assert str(A**3) == "A**3"


def test_MatrixSymbol_printing():
    # test cases for issue #14237
    A = MatrixSymbol("A", 3, 3)
    B = MatrixSymbol("B", 3, 3)
    C = MatrixSymbol("C", 3, 3)
    assert pretty(-A*B*C) == "-A*B*C"
    assert pretty(A - B) == "-B + A"
    assert pretty(A*B*C - A*B - B*C) == "-A*B -B*C + A*B*C"

    # issue #14814
    x = MatrixSymbol('x', n, n)
    y = MatrixSymbol('y*', n, n)
    assert pretty(x + y) == "x + y*"
    ascii_str = \
"""\
     2     \n\
-2*y*  -a*x\
"""
    assert pretty(-a*x + -2*y*y) == ascii_str

