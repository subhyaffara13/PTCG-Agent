
def test_issue_10472():
    M = (Matrix([[0, 0], [0, 0]]), Matrix([0, 0]))

    ucode_str = \
"""\
⎛⎡0  0⎤  ⎡0⎤⎞
⎜⎢    ⎥, ⎢ ⎥⎟
⎝⎣0  0⎦  ⎣0⎦⎠\
"""
    assert upretty(M) == ucode_str

