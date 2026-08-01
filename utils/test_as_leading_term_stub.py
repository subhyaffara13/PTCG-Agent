
def test_as_leading_term_stub():
    class foo(Function):
        pass
    assert foo(1/x).as_leading_term(x) == foo(1/x)
    assert foo(1).as_leading_term(x) == foo(1)
    raises(NotImplementedError, lambda: foo(x).as_leading_term(x))

