
def test_rmul_pr19860():
    class Foo(ImmutableDenseMatrix):
        _op_priority = MutableDenseMatrix._op_priority + 0.01

    a = Matrix(2, 2, [1, 2, 3, 4])
    b = Foo(2, 2, [1, 2, 3, 4])

    # This would throw a RecursionError: maximum recursion depth
    # since b always has higher priority even after a.as_mutable()
    c = a*b

    assert isinstance(c, Foo)
    assert c == Matrix([[7, 10], [15, 22]])


def test_rmul_pr19860():
    class Foo(ImmutableDenseMatrix):
        _op_priority = MutableDenseMatrix._op_priority + 0.01

    a = Matrix(2, 2, [1, 2, 3, 4])
    b = Foo(2, 2, [1, 2, 3, 4])

    # This would throw a RecursionError: maximum recursion depth
    # since b always has higher priority even after a.as_mutable()
    c = a*b

    assert isinstance(c, Foo)
    assert c == Matrix([[7, 10], [15, 22]])

