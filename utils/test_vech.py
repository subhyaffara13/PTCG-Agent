
def test_vech():
    m = Matrix([[1, 2], [2, 3]])
    m_vech = m.vech()
    assert m_vech.cols == 1
    for i in range(3):
        assert m_vech[i] == i + 1
    m_vech = m.vech(diagonal=False)
    assert m_vech[0] == 2

    m = Matrix([[1, x*(x + y)], [y*x + x**2, 1]])
    m_vech = m.vech(diagonal=False)
    assert m_vech[0] == y*x + x**2

    m = Matrix([[1, x*(x + y)], [y*x, 1]])
    m_vech = m.vech(diagonal=False, check_symmetry=False)
    assert m_vech[0] == y*x

    raises(ShapeError, lambda: Matrix([[1, 3]]).vech())
    raises(ValueError, lambda: Matrix([[1, 3], [2, 4]]).vech())
    raises(ShapeError, lambda: Matrix([[1, 3]]).vech())
    raises(ValueError, lambda: Matrix([[1, 3], [2, 4]]).vech())


def test_vech():
    m = Matrix([[1, 2], [2, 3]])
    m_vech = m.vech()
    assert m_vech.cols == 1
    for i in range(3):
        assert m_vech[i] == i + 1
    m_vech = m.vech(diagonal=False)
    assert m_vech[0] == 2

    m = Matrix([[1, x*(x + y)], [y*x + x**2, 1]])
    m_vech = m.vech(diagonal=False)
    assert m_vech[0] == y*x + x**2

    m = Matrix([[1, x*(x + y)], [y*x, 1]])
    m_vech = m.vech(diagonal=False, check_symmetry=False)
    assert m_vech[0] == y*x

    raises(ShapeError, lambda: Matrix([[1, 3]]).vech())
    raises(ValueError, lambda: Matrix([[1, 3], [2, 4]]).vech())
    raises(ShapeError, lambda: Matrix([[1, 3]]).vech())
    raises(ValueError, lambda: Matrix([[1, 3], [2, 4]]).vech())

