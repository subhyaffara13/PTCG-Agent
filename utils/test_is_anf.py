
def test_is_anf():
    x, y = symbols('x,y')
    assert is_anf(true) is True
    assert is_anf(false) is True
    assert is_anf(x) is True
    assert is_anf(And(x, y)) is True
    assert is_anf(Xor(x, y, And(x, y))) is True
    assert is_anf(Xor(x, y, Or(x, y))) is False
    assert is_anf(Xor(Not(x), y)) is False

