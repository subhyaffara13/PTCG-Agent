
def test_companion():
    x = Symbol('x')
    y = Symbol('y')
    raises(ValueError, lambda: Matrix.companion(1))
    raises(ValueError, lambda: Matrix.companion(Poly([1], x)))
    raises(ValueError, lambda: Matrix.companion(Poly([2, 1], x)))
    raises(ValueError, lambda: Matrix.companion(Poly(x*y, [x, y])))

    c0, c1, c2 = symbols('c0:3')
    assert Matrix.companion(Poly([1, c0], x)) == Matrix([-c0])
    assert Matrix.companion(Poly([1, c1, c0], x)) == \
        Matrix([[0, -c0], [1, -c1]])
    assert Matrix.companion(Poly([1, c2, c1, c0], x)) == \
        Matrix([[0, 0, -c0], [1, 0, -c1], [0, 1, -c2]])


def test_companion():
    x = Symbol('x')
    y = Symbol('y')
    raises(ValueError, lambda: Matrix.companion(1))
    raises(ValueError, lambda: Matrix.companion(Poly([1], x)))
    raises(ValueError, lambda: Matrix.companion(Poly([2, 1], x)))
    raises(ValueError, lambda: Matrix.companion(Poly(x*y, [x, y])))

    c0, c1, c2 = symbols('c0:3')
    assert Matrix.companion(Poly([1, c0], x)) == Matrix([-c0])
    assert Matrix.companion(Poly([1, c1, c0], x)) == \
        Matrix([[0, -c0], [1, -c1]])
    assert Matrix.companion(Poly([1, c2, c1, c0], x)) == \
        Matrix([[0, 0, -c0], [1, 0, -c1], [0, 1, -c2]])

