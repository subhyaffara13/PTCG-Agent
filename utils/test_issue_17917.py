
def test_issue_17917():
    X = R2.x*R2.e_x - R2.y*R2.e_y
    Y = (R2.x**2 + R2.y**2)*R2.e_x - R2.x*R2.y*R2.e_y
    assert LieDerivative(X, Y).expand() == (
        R2.x**2*R2.e_x - 3*R2.y**2*R2.e_x - R2.x*R2.y*R2.e_y)

