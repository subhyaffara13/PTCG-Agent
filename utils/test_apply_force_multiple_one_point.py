
def test_apply_force_multiple_one_point():
    a, b = symbols('a b')
    P = Point('P')
    with warns_deprecated_sympy():
        B = Body('B')
    f1 = a*B.x
    f2 = b*B.y
    B.apply_force(f1, P)
    assert B.loads == [(P, f1)]
    B.apply_force(f2, P)
    assert B.loads == [(P, f1+f2)]

