
def test_MatrixExpressions():
    n = Symbol('n', integer=True)
    X = MatrixSymbol('X', n, n)

    assert str(X) == "X"

    # Apply function elementwise (`ElementwiseApplyFunc`):

    expr = (X.T*X).applyfunc(sin)
    assert str(expr) == 'Lambda(_d, sin(_d)).(X.T*X)'

    lamda = Lambda(x, 1/x)
    expr = (n*X).applyfunc(lamda)
    assert str(expr) == 'Lambda(x, 1/x).(n*X)'


def test_MatrixExpressions():
    n = Symbol('n', integer=True)
    X = MatrixSymbol('X', n, n)

    assert pretty(X) == upretty(X) == "X"

    # Apply function elementwise (`ElementwiseApplyFunc`):

    expr = (X.T*X).applyfunc(sin)

    ascii_str = """\
              / T  \\\n\
(d -> sin(d)).\\X *X/\
"""
    ucode_str = """\
             ⎛ T  ⎞\n\
(d ↦ sin(d))˳⎝X ⋅X⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    lamda = Lambda(x, 1/x)
    expr = (n*X).applyfunc(lamda)
    ascii_str = """\
/     1\\      \n\
|x -> -|.(n*X)\n\
\\     x/      \
"""
    ucode_str = """\
⎛    1⎞      \n\
⎜x ↦ ─⎟˳(n⋅X)\n\
⎝    x⎠      \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

