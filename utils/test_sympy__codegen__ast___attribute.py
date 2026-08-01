
def test_sympy__codegen__ast__Attribute():
    from sympy.codegen.ast import Attribute
    assert _test_args(Attribute('noexcept'))

