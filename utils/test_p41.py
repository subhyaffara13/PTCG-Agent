
def test_P41():
    r, t = symbols('r t', real=True)
    assert hessian(r**2*sin(t),(r,t)) == Matrix([[  2*sin(t),   2*r*cos(t)],
                                                 [2*r*cos(t), -r**2*sin(t)]])

