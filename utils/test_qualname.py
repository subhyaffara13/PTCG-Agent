
def test_qualname(doc):
    """Tests that a properly qualified name is set in __qualname__ and that
    generated docstrings properly use it and the module name"""
    assert m.NestBase.__qualname__ == "NestBase"
    assert m.NestBase.Nested.__qualname__ == "NestBase.Nested"

    assert (
        doc(m.NestBase.__init__)
        == """
        __init__(self: m.class_.NestBase) -> None
    """
    )
    assert (
        doc(m.NestBase.g)
        == """
        g(self: m.class_.NestBase, arg0: m.class_.NestBase.Nested) -> None
    """
    )
    assert (
        doc(m.NestBase.Nested.__init__)
        == """
        __init__(self: m.class_.NestBase.Nested) -> None
    """
    )
    assert (
        doc(m.NestBase.Nested.fn)
        == """
        fn(self: m.class_.NestBase.Nested, arg0: int, arg1: m.class_.NestBase, arg2: m.class_.NestBase.Nested) -> None
    """
    )
    assert (
        doc(m.NestBase.Nested.fa)
        == """
        fa(self: m.class_.NestBase.Nested, a: int, b: m.class_.NestBase, c: m.class_.NestBase.Nested) -> None
    """
    )
    assert m.NestBase.__module__ == "pybind11_tests.class_"
    assert m.NestBase.Nested.__module__ == "pybind11_tests.class_"

