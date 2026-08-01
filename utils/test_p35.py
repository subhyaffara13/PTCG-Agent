
def test_P35():
    M = pi/2*Matrix([[2, 1, 1],
                     [2, 3, 2],
                     [1, 1, 2]])
    # raises exception, sin(M) not supported. exp(M*I) also not supported
    # https://github.com/sympy/sympy/issues/6218
    assert sin(M) == eye(3)

