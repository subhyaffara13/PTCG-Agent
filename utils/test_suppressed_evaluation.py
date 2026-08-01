
def test_suppressed_evaluation():
    a = Add(0, 3, 2, evaluate=False)
    b = Mul(1, 3, 2, evaluate=False)
    c = Pow(3, 2, evaluate=False)
    assert a != 6
    assert a.func is Add
    assert a.args == (0, 3, 2)
    assert b != 6
    assert b.func is Mul
    assert b.args == (1, 3, 2)
    assert c != 9
    assert c.func is Pow
    assert c.args == (3, 2)


def test_suppressed_evaluation():
    a = sin(0, evaluate=False)
    assert a != 0
    assert a.func is sin
    assert a.args == (0,)

