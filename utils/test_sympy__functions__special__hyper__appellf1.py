
def test_sympy__functions__special__hyper__appellf1():
    from sympy.functions.special.hyper import appellf1
    a, b1, b2, c, x, y = symbols('a b1 b2 c x y')
    assert _test_args(appellf1(a, b1, b2, c, x, y))

