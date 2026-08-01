
def test_Add_is_algebraic():
    a = Symbol('a', algebraic=True)
    b = Symbol('a', algebraic=True)
    na = Symbol('na', algebraic=False)
    nb = Symbol('nb', algebraic=False)
    x = Symbol('x')
    assert (a + b).is_algebraic
    assert (na + nb).is_algebraic is None
    assert (a + na).is_algebraic is False
    assert (a + x).is_algebraic is None
    assert (na + x).is_algebraic is None

