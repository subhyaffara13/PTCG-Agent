
def test_sympy__functions__combinatorial__factorials__FallingFactorial():
    from sympy.functions.combinatorial.factorials import FallingFactorial
    assert _test_args(FallingFactorial(2, x))

