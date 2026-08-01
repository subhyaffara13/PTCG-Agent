
def test_format_sympy():
    for test in _tests:
        lhs = represent(test[0], basis=A, format='sympy')
        rhs = to_sympy(test[1])
        assert lhs == rhs

