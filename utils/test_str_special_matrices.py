
def test_str_special_matrices():
    from sympy.matrices import Identity, ZeroMatrix, OneMatrix
    assert str(Identity(4)) == 'I'
    assert str(ZeroMatrix(2, 2)) == '0'
    assert str(OneMatrix(2, 2)) == '1'


def test_str_special_matrices():
    from sympy.matrices import Identity, ZeroMatrix, OneMatrix
    assert pretty(Identity(4)) == 'I'
    assert upretty(Identity(4)) == '𝕀'
    assert pretty(ZeroMatrix(2, 2)) == '0'
    assert upretty(ZeroMatrix(2, 2)) == '𝟘'
    assert pretty(OneMatrix(2, 2)) == '1'
    assert upretty(OneMatrix(2, 2)) == '𝟙'

