
def test_Str():
    from sympy.core.symbol import Str
    assert str(Str('x')) == r'x'


def test_Str():
    from sympy.core.symbol import Str
    assert str(Str('x')) == 'x'
    assert sstrrepr(Str('x')) == "Str('x')"


def test_Str():
    from sympy.core.symbol import Str
    assert pretty(Str('x')) == 'x'


def test_Str():
    a1 = Str('a')
    a2 = Str('a')
    b = Str('b')
    assert a1 == a2 != b
    raises(TypeError, lambda: Str())

