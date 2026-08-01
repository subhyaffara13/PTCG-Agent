
def test_sympy__functions__special__mathieu_functions__mathieucprime():
    from sympy.functions.special.mathieu_functions import mathieucprime
    assert _test_args(mathieucprime(1, 1, 1))

