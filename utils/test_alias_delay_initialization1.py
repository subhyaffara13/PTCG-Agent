
def test_alias_delay_initialization1(capture):
    """`A` only initializes its trampoline class when we inherit from it

    If we just create and use an A instance directly, the trampoline initialization is
    bypassed and we only initialize an A() instead (for performance reasons).
    """

    class B(m.A):
        def __init__(self):
            super().__init__()

        def f(self):
            print("In python f()")

    # C++ version
    with capture:
        a = m.A()
        m.call_f(a)
        del a
        pytest.gc_collect()
    assert capture == "A.f()"

    # Python version
    with capture:
        b = B()
        m.call_f(b)
        del b
        pytest.gc_collect()
    assert (
        capture
        == """
        PyA.PyA()
        PyA.f()
        In python f()
        PyA.~PyA()
    """
    )

