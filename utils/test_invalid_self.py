
def test_invalid_self():
    """Tests invocation of the pybind-registered base class with an invalid `self` argument."""

    class NotPybindDerived:
        pass

    # Attempts to initialize with an invalid type passed as `self`:
    class BrokenTF1(m.TestFactory1):
        def __init__(self, bad):
            if bad == 1:
                a = m.TestFactory2(tag.pointer, 1)
                m.TestFactory1.__init__(a, tag.pointer)
            elif bad == 2:
                a = NotPybindDerived()
                m.TestFactory1.__init__(a, tag.pointer)

    # Same as above, but for a class with an alias:
    class BrokenTF6(m.TestFactory6):
        def __init__(self, bad):
            if bad == 0:
                m.TestFactory6.__init__()
            elif bad == 1:
                a = m.TestFactory2(tag.pointer, 1)
                m.TestFactory6.__init__(a, tag.base, 1)
            elif bad == 2:
                a = m.TestFactory2(tag.pointer, 1)
                m.TestFactory6.__init__(a, tag.alias, 1)
            elif bad == 3:
                m.TestFactory6.__init__(
                    NotPybindDerived.__new__(NotPybindDerived), tag.base, 1
                )
            elif bad == 4:
                m.TestFactory6.__init__(
                    NotPybindDerived.__new__(NotPybindDerived), tag.alias, 1
                )

    for arg in (1, 2):
        with pytest.raises(TypeError) as excinfo:
            BrokenTF1(arg)
        assert (
            str(excinfo.value)
            == "__init__(self, ...) called with invalid or missing `self` argument"
        )

    for arg in (0, 1, 2, 3, 4):
        with pytest.raises(TypeError) as excinfo:
            BrokenTF6(arg)
        assert (
            str(excinfo.value)
            == "__init__(self, ...) called with invalid or missing `self` argument"
        )

