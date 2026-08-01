
def test_attr():
    import attr
    @attr.s
    class A:
        a = attr.ib()

    v = A(1)
    assert dill.copy(v) == v

