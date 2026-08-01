
def test_linear_eq_to_matrix():
    assert linear_eq_to_matrix(0, x) == (Matrix([[0]]), Matrix([[0]]))
    assert linear_eq_to_matrix(1, x) == (Matrix([[0]]), Matrix([[-1]]))

    # integer coefficients
    eqns1 = [2*x + y - 2*z - 3, x - y - z, x + y + 3*z - 12]
    eqns2 = [Eq(3*x + 2*y - z, 1), Eq(2*x - 2*y + 4*z, -2), -2*x + y - 2*z]

    A, B = linear_eq_to_matrix(eqns1, x, y, z)
    assert A == Matrix([[2, 1, -2], [1, -1, -1], [1, 1, 3]])
    assert B == Matrix([[3], [0], [12]])

    A, B = linear_eq_to_matrix(eqns2, x, y, z)
    assert A == Matrix([[3, 2, -1], [2, -2, 4], [-2, 1, -2]])
    assert B == Matrix([[1], [-2], [0]])

    # Pure symbolic coefficients
    eqns3 = [a*b*x + b*y + c*z - d, e*x + d*x + f*y + g*z - h, i*x + j*y + k*z - l]
    A, B = linear_eq_to_matrix(eqns3, x, y, z)
    assert A == Matrix([[a*b, b, c], [d + e, f, g], [i, j, k]])
    assert B == Matrix([[d], [h], [l]])

    # raise Errors if
    # 1) no symbols are given
    raises(ValueError, lambda: linear_eq_to_matrix(eqns3))
    # 2) there are duplicates
    raises(ValueError, lambda: linear_eq_to_matrix(eqns3, [x, x, y]))
    # 3) a nonlinear term is detected in the original expression
    raises(NonlinearError, lambda: linear_eq_to_matrix(Eq(1/x + x, 1/x), [x]))
    raises(NonlinearError, lambda: linear_eq_to_matrix([x**2], [x]))
    raises(NonlinearError, lambda: linear_eq_to_matrix([x*y], [x, y]))
    # 4) Eq being used to represent equations autoevaluates
    # (use unevaluated Eq instead)
    raises(ValueError, lambda: linear_eq_to_matrix(Eq(x, x), x))
    raises(ValueError, lambda: linear_eq_to_matrix(Eq(x, x + 1), x))


    # if non-symbols are passed, the user is responsible for interpreting
    assert linear_eq_to_matrix([x], [1/x]) == (Matrix([[0]]), Matrix([[-x]]))

    # issue 15195
    assert linear_eq_to_matrix(x + y*(z*(3*x + 2) + 3), x) == (
        Matrix([[3*y*z + 1]]), Matrix([[-y*(2*z + 3)]]))
    assert linear_eq_to_matrix(Matrix(
        [[a*x + b*y - 7], [5*x + 6*y - c]]), x, y) == (
        Matrix([[a, b], [5, 6]]), Matrix([[7], [c]]))

    # issue 15312
    assert linear_eq_to_matrix(Eq(x + 2, 1), x) == (
        Matrix([[1]]), Matrix([[-1]]))

    # issue 25423
    raises(TypeError, lambda: linear_eq_to_matrix([], {x, y}))
    raises(TypeError, lambda: linear_eq_to_matrix([x + y], {x, y}))
    raises(ValueError, lambda: linear_eq_to_matrix({x + y}, (x, y)))

