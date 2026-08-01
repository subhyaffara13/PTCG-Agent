
def test_alias_delay_initialization2(capture):
    """`A2`, unlike the above, is configured to always initialize the alias

    While the extra initialization and extra class layer has small virtual dispatch
    performance penalty, it also allows us to do more things with the trampoline
    class such as defining local variables and performing construction/destruction.
    """

    class B2(m.A2):
        def __init__(self):
            super().__init__()

        def f(self):
            print("In python B2.f()")

    # No python subclass version
    with capture:
        a2 = m.A2()
        m.call_f(a2)
        del a2
        pytest.gc_collect()
        a3 = m.A2(1)
        m.call_f(a3)
        del a3
        pytest.gc_collect()
    assert (
        capture
        == """
        PyA2.PyA2()
        PyA2.f()
        A2.f()
        PyA2.~PyA2()
        PyA2.PyA2()
        PyA2.f()
        A2.f()
        PyA2.~PyA2()
    """
    )

    # Python subclass version
    with capture:
        b2 = B2()
        m.call_f(b2)
        del b2
        pytest.gc_collect()
    assert (
        capture
        == """
        PyA2.PyA2()
        PyA2.f()
        In python B2.f()
        PyA2.~PyA2()
    """
    )

