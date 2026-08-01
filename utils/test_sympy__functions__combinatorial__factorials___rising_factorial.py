
def test_sympy__functions__combinatorial__factorials__RisingFactorial():
    from sympy.functions.combinatorial.factorials import RisingFactorial
    assert _test_args(RisingFactorial(2, x))

