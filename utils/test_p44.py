
def test_P44():
    def __my_hessian(f, Y):
        V = Matrix([diff(f, v) for v in Y])
        return  Matrix([V.T.diff(v) for v in Y])
    r, t = symbols('r t', real=True)
    assert __my_hessian(r**2*sin(t), (r, t)) == Matrix([
                                            [  2*sin(t),   2*r*cos(t)],
                                            [2*r*cos(t), -r**2*sin(t)]])

