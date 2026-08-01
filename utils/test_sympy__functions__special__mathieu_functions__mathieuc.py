
def test_sympy__functions__special__mathieu_functions__mathieuc():
    from sympy.functions.special.mathieu_functions import mathieuc
    assert _test_args(mathieuc(1, 1, 1))

