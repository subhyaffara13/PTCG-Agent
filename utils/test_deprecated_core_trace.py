
def test_deprecated_core_trace():
    with warns_deprecated_sympy():
        from sympy.core.trace import Tr # noqa:F401

