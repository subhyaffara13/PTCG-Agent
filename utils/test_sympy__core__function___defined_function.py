
def test_sympy__core__function__DefinedFunction():
    from sympy.core.function import DefinedFunction
    assert _test_args(DefinedFunction(1, 2, 3))

