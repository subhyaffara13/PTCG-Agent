
def test_clear_load():
    a = symbols('a')
    P = Point('P')
    with warns_deprecated_sympy():
        B = Body('B')
    force = a*B.z
    B.apply_force(force, P)
    assert B.loads == [(P, force)]
    B.clear_loads()
    assert B.loads == []

