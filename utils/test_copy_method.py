
def test_copy_method():
    """Issue #443: calling copied methods fails in Python 3"""

    m.ExampleMandA.add2c = m.ExampleMandA.add2
    m.ExampleMandA.add2d = m.ExampleMandA.add2b
    a = m.ExampleMandA(123)
    assert a.value == 123
    a.add2(m.ExampleMandA(-100))
    assert a.value == 23
    a.add2b(m.ExampleMandA(20))
    assert a.value == 43
    a.add2c(m.ExampleMandA(6))
    assert a.value == 49
    a.add2d(m.ExampleMandA(-7))
    assert a.value == 42


def test_copy_method(deep):
    idx = MultiIndex(
        levels=[["foo", "bar"], ["fizz", "buzz"]],
        codes=[[0, 0, 0, 1], [0, 0, 1, 1]],
        names=["first", "second"],
    )
    idx_copy = idx.copy(deep=deep)
    assert idx_copy.equals(idx)

