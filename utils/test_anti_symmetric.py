
def test_anti_symmetric():
    assert Matrix([1, 2]).is_anti_symmetric() is False
    m = Matrix(3, 3, [0, x**2 + 2*x + 1, y, -(x + 1)**2, 0, x*y, -y, -x*y, 0])
    assert m.is_anti_symmetric() is True
    assert m.is_anti_symmetric(simplify=False) is None
    assert m.is_anti_symmetric(simplify=lambda x: x) is None

    # tweak to fail
    m[2, 1] = -m[2, 1]
    assert m.is_anti_symmetric() is None
    # untweak
    m[2, 1] = -m[2, 1]

    m = m.expand()
    assert m.is_anti_symmetric(simplify=False) is True
    m[0, 0] = 1
    assert m.is_anti_symmetric() is False


def test_anti_symmetric():
    assert Matrix([1, 2]).is_anti_symmetric() is False
    m = Matrix(3, 3, [0, x**2 + 2*x + 1, y, -(x + 1)**2, 0, x*y, -y, -x*y, 0])
    assert m.is_anti_symmetric() is True
    assert m.is_anti_symmetric(simplify=False) is None
    assert m.is_anti_symmetric(simplify=lambda x: x) is None

    # tweak to fail
    m[2, 1] = -m[2, 1]
    assert m.is_anti_symmetric() is None
    # untweak
    m[2, 1] = -m[2, 1]

    m = m.expand()
    assert m.is_anti_symmetric(simplify=False) is True
    m[0, 0] = 1
    assert m.is_anti_symmetric() is False

