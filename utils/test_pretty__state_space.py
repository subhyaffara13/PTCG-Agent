
def test_pretty_StateSpace():
    ss1 = StateSpace(Matrix([a]), Matrix([b]), Matrix([c]), Matrix([d]))
    A = Matrix([[0, 1], [1, 0]])
    B = Matrix([1, 0])
    C = Matrix([[0, 1]])
    D = Matrix([0])
    ss2 = StateSpace(A, B, C, D)
    ss3 = StateSpace(Matrix([[-1.5, -2], [1, 0]]),
                    Matrix([[0.5, 0], [0, 1]]),
                    Matrix([[0, 1], [0, 2]]),
                    Matrix([[2, 2], [1, 1]]))

    expected1 = \
"""\
⎡[a]  [b]⎤\n\
⎢        ⎥\n\
⎣[c]  [d]⎦\
"""
    expected2 = \
"""\
⎡⎡0  1⎤  ⎡1⎤⎤\n\
⎢⎢    ⎥  ⎢ ⎥⎥\n\
⎢⎣1  0⎦  ⎣0⎦⎥\n\
⎢           ⎥\n\
⎣[0  1]  [0]⎦\
"""
    expected3 = \
"""\
⎡⎡-1.5  -2⎤  ⎡0.5  0⎤⎤\n\
⎢⎢        ⎥  ⎢      ⎥⎥\n\
⎢⎣ 1    0 ⎦  ⎣ 0   1⎦⎥\n\
⎢                    ⎥\n\
⎢  ⎡0  1⎤     ⎡2  2⎤ ⎥\n\
⎢  ⎢    ⎥     ⎢    ⎥ ⎥\n\
⎣  ⎣0  2⎦     ⎣1  1⎦ ⎦\
"""

    assert upretty(ss1) == expected1
    assert upretty(ss2) == expected2
    assert upretty(ss3) == expected3

