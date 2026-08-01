
def test_sympy__functions__special__mathieu_functions__mathieus():
    from sympy.functions.special.mathieu_functions import mathieus
    assert _test_args(mathieus(1, 1, 1))

