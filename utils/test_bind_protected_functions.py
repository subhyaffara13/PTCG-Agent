
def test_bind_protected_functions():
    """Expose protected member functions to Python using a helper class"""
    a = m.ProtectedA()
    assert a.foo() == 42

    b = m.ProtectedB()
    assert b.foo() == 42
    assert m.read_foo(b.void_foo()) == 42
    assert m.pointers_equal(b.get_self(), b)

    class C(m.ProtectedB):
        def __init__(self):
            m.ProtectedB.__init__(self)

        def foo(self):
            return 0

    c = C()
    assert c.foo() == 0

