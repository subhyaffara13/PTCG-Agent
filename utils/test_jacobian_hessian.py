
def test_jacobian_hessian():
    L = Matrix(1, 2, [x**2*y, 2*y**2 + x*y])
    syms = [x, y]
    assert _forward_jacobian(L, syms) == Matrix([[2*x*y, x**2], [y, 4*y + x]])

    L = Matrix(1, 2, [x, x**2*y**3])
    assert _forward_jacobian(L, syms) == Matrix([[1, 0], [2*x*y**3, x**2*3*y**2]])


def test_jacobian_hessian():
    L = Matrix(1, 2, [x**2*y, 2*y**2 + x*y])
    syms = [x, y]
    assert L.jacobian(syms) == Matrix([[2*x*y, x**2], [y, 4*y + x]])

    L = Matrix(1, 2, [x, x**2*y**3])
    assert L.jacobian(syms) == Matrix([[1, 0], [2*x*y**3, x**2*3*y**2]])

    f = x**2*y
    syms = [x, y]
    assert hessian(f, syms) == Matrix([[2*y, 2*x], [2*x, 0]])

    f = x**2*y**3
    assert hessian(f, syms) == \
        Matrix([[2*y**3, 6*x*y**2], [6*x*y**2, 6*x**2*y]])

    f = z + x*y**2
    g = x**2 + 2*y**3
    ans = Matrix([[0,   2*y],
                  [2*y, 2*x]])
    assert ans == hessian(f, Matrix([x, y]))
    assert ans == hessian(f, Matrix([x, y]).T)
    assert hessian(f, (y, x), [g]) == Matrix([
        [     0, 6*y**2, 2*x],
        [6*y**2,    2*x, 2*y],
        [   2*x,    2*y,   0]])


def test_jacobian_hessian():
    L = Matrix(1, 2, [x**2*y, 2*y**2 + x*y])
    syms = [x, y]
    assert L.jacobian(syms) == Matrix([[2*x*y, x**2], [y, 4*y + x]])

    L = Matrix(1, 2, [x, x**2*y**3])
    assert L.jacobian(syms) == Matrix([[1, 0], [2*x*y**3, x**2*3*y**2]])

    f = x**2*y
    syms = [x, y]
    assert hessian(f, syms) == Matrix([[2*y, 2*x], [2*x, 0]])

    f = x**2*y**3
    assert hessian(f, syms) == \
        Matrix([[2*y**3, 6*x*y**2], [6*x*y**2, 6*x**2*y]])

    f = z + x*y**2
    g = x**2 + 2*y**3
    ans = Matrix([[0,   2*y],
                  [2*y, 2*x]])
    assert ans == hessian(f, Matrix([x, y]))
    assert ans == hessian(f, Matrix([x, y]).T)
    assert hessian(f, (y, x), [g]) == Matrix([
        [     0, 6*y**2, 2*x],
        [6*y**2,    2*x, 2*y],
        [   2*x,    2*y,   0]])

