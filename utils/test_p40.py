
def test_P40():
    r, t = symbols('r t', real=True)
    M = Matrix([r*cos(t), r*sin(t)])
    assert M.jacobian(Matrix([r, t])) == Matrix([[cos(t), -r*sin(t)],
                                                 [sin(t),  r*cos(t)]])

