
def test_P43():
    def __my_jacobian(M, Y):
        return Matrix([M.diff(v).T for v in Y]).T
    r, t = symbols('r t', real=True)
    M = Matrix([r*cos(t), r*sin(t)])
    assert __my_jacobian(M,[r,t]) == Matrix([[cos(t), -r*sin(t)],
                                             [sin(t),  r*cos(t)]])

