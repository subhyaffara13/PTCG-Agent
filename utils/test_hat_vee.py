
def test_hat_vee():
    v1 = Matrix([x, y, z])
    v2 = Matrix([a, b, c])
    assert v1.hat() * v2 == v1.cross(v2)
    assert v1.hat().is_anti_symmetric()
    assert v1.hat().vee() == v1


def test_hat_vee():
    v1 = Matrix([x, y, z])
    v2 = Matrix([a, b, c])
    assert v1.hat() * v2 == v1.cross(v2)
    assert v1.hat().is_anti_symmetric()
    assert v1.hat().vee() == v1

