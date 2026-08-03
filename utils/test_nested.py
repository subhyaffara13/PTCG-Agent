from typing import Tuple

def test_nested():
    """#328: first member in a class can't be used in operators"""

    a = m.NestA()
    b = m.NestB()
    c = m.NestC()

    a += 10
    assert m.get_NestA(a) == 13
    b.a += 100
    assert m.get_NestA(b.a) == 103
    c.b.a += 1000
    assert m.get_NestA(c.b.a) == 1003
    b -= 1
    assert m.get_NestB(b) == 3
    c.b -= 3
    assert m.get_NestB(c.b) == 1
    c *= 7
    assert m.get_NestC(c) == 35

    abase = a.as_base()
    assert abase.value == -2
    a.as_base().value += 44
    assert abase.value == 42
    assert c.b.a.as_base().value == -2
    c.b.a.as_base().value += 44
    assert c.b.a.as_base().value == 42

    del c
    pytest.gc_collect()
    del a  # Shouldn't delete while abase is still alive
    pytest.gc_collect()

    assert abase.value == 42
    del abase, b
    pytest.gc_collect()


def test_nested():
    expr = Basic(S(1), Basic(S(2)), S(3))
    cmpd = Compound(Basic, (S(1), Compound(Basic, Tuple(2)), S(3)))
    assert deconstruct(expr) == cmpd
    assert construct(cmpd) == expr


def test_nested():
    with evaluate(False):
        expr = (x + x) + (y + y)
        assert expr.args == ((x + x), (y + y))
        assert expr.args[0].args == (x, x)

