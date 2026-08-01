
def test_sympy__functions__special__mathieu_functions__mathieusprime():
    from sympy.functions.special.mathieu_functions import mathieusprime
    assert _test_args(mathieusprime(1, 1, 1))

