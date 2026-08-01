
def test_sympy__physics__optics__waves__TWave():
    from sympy.physics.optics import TWave
    A, f, phi = symbols('A, f, phi')
    assert _test_args(TWave(A, f, phi))

