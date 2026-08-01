
def test_P34():
    a, b, c = symbols('a b c', real=True)
    M = Matrix([[a, 1, 0, 0, 0, 0],
                [0, a, 0, 0, 0, 0],
                [0, 0, b, 0, 0, 0],
                [0, 0, 0, c, 1, 0],
                [0, 0, 0, 0, c, 1],
                [0, 0, 0, 0, 0, c]])
    # raises exception, sin(M) not supported. exp(M*I) also not supported
    # https://github.com/sympy/sympy/issues/6218
    assert sin(M) == Matrix([[sin(a), cos(a), 0, 0, 0, 0],
                             [0, sin(a), 0, 0, 0, 0],
                             [0, 0, sin(b), 0, 0, 0],
                             [0, 0, 0, sin(c), cos(c), -sin(c)/2],
                             [0, 0, 0, 0, sin(c), cos(c)],
                             [0, 0, 0, 0, 0, sin(c)]])

