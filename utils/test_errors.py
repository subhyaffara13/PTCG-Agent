
def test_errors():
    if not matplotlib:
        skip("Matplotlib not the default backend")

    # Invalid `system` check
    tfm = TransferFunctionMatrix([[tf6, tf5], [tf5, tf6]])
    expr = 1/(s**2 - 1)
    raises(NotImplementedError, lambda: pole_zero_plot(tfm))
    raises(NotImplementedError, lambda: pole_zero_numerical_data(expr))
    raises(NotImplementedError, lambda: impulse_response_plot(expr))
    raises(NotImplementedError, lambda: impulse_response_numerical_data(tfm))
    raises(NotImplementedError, lambda: step_response_plot(tfm))
    raises(NotImplementedError, lambda: step_response_numerical_data(expr))
    raises(NotImplementedError, lambda: ramp_response_plot(expr))
    raises(NotImplementedError, lambda: ramp_response_numerical_data(tfm))
    raises(NotImplementedError, lambda: bode_plot(tfm))

    # More than 1 variables
    tf_a = TransferFunction(a, s + 1, s)
    raises(ValueError, lambda: pole_zero_plot(tf_a))
    raises(ValueError, lambda: pole_zero_numerical_data(tf_a))
    raises(ValueError, lambda: impulse_response_plot(tf_a))
    raises(ValueError, lambda: impulse_response_numerical_data(tf_a))
    raises(ValueError, lambda: step_response_plot(tf_a))
    raises(ValueError, lambda: step_response_numerical_data(tf_a))
    raises(ValueError, lambda: ramp_response_plot(tf_a))
    raises(ValueError, lambda: ramp_response_numerical_data(tf_a))
    raises(ValueError, lambda: bode_plot(tf_a))

    # lower_limit > 0 for response plots
    raises(ValueError, lambda: impulse_response_plot(tf1, lower_limit=-1))
    raises(ValueError, lambda: step_response_plot(tf1, lower_limit=-0.1))
    raises(ValueError, lambda: ramp_response_plot(tf1, lower_limit=-4/3))

    # slope in ramp_response_plot() is negative
    raises(ValueError, lambda: ramp_response_plot(tf1, slope=-0.1))

    # incorrect frequency or phase unit
    raises(ValueError, lambda: bode_plot(tf1,freq_unit = 'hz'))
    raises(ValueError, lambda: bode_plot(tf1,phase_unit = 'degree'))


def test_errors():
    raises(ValueError, lambda: Matrix([[1, 2], [1]]))
    raises(IndexError, lambda: Matrix([[1, 2]])[1.2, 5])
    raises(IndexError, lambda: Matrix([[1, 2]])[1, 5.2])
    raises(ValueError, lambda: randMatrix(3, c=4, symmetric=True))
    raises(ValueError, lambda: Matrix([1, 2]).reshape(4, 6))
    raises(ShapeError,
        lambda: Matrix([[1, 2], [3, 4]]).copyin_matrix([1, 0], Matrix([1, 2])))
    raises(TypeError, lambda: Matrix([[1, 2], [3, 4]]).copyin_list([0,
           1], set()))
    raises(NonSquareMatrixError, lambda: Matrix([[1, 2, 3], [2, 3, 0]]).inv())
    raises(ShapeError,
        lambda: Matrix(1, 2, [1, 2]).row_join(Matrix([[1, 2], [3, 4]])))
    raises(
        ShapeError, lambda: Matrix([1, 2]).col_join(Matrix([[1, 2], [3, 4]])))
    raises(ShapeError, lambda: Matrix([1]).row_insert(1, Matrix([[1,
           2], [3, 4]])))
    raises(ShapeError, lambda: Matrix([1]).col_insert(1, Matrix([[1,
           2], [3, 4]])))
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).trace())
    raises(TypeError, lambda: Matrix([1]).applyfunc(1))
    raises(ValueError, lambda: Matrix([[1, 2], [3, 4]]).minor(4, 5))
    raises(ValueError, lambda: Matrix([[1, 2], [3, 4]]).minor_submatrix(4, 5))
    raises(TypeError, lambda: Matrix([1, 2, 3]).cross(1))
    raises(TypeError, lambda: Matrix([1, 2, 3]).dot(1))
    raises(ShapeError, lambda: Matrix([1, 2, 3]).dot(Matrix([1, 2])))
    raises(ShapeError, lambda: Matrix([1, 2]).dot([]))
    raises(TypeError, lambda: Matrix([1, 2]).dot('a'))
    raises(ShapeError, lambda: Matrix([1, 2]).dot([1, 2, 3]))
    raises(NonSquareMatrixError, lambda: Matrix([1, 2, 3]).exp())
    raises(ShapeError, lambda: Matrix([[1, 2], [3, 4]]).normalized())
    raises(ValueError, lambda: Matrix([1, 2]).inv(method='not a method'))
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).inverse_GE())
    raises(ValueError, lambda: Matrix([[1, 2], [1, 2]]).inverse_GE())
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).inverse_ADJ())
    raises(ValueError, lambda: Matrix([[1, 2], [1, 2]]).inverse_ADJ())
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).inverse_LU())
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).is_nilpotent())
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).det())
    raises(ValueError,
        lambda: Matrix([[1, 2], [3, 4]]).det(method='Not a real method'))
    raises(ValueError,
        lambda: Matrix([[1, 2, 3, 4], [5, 6, 7, 8],
        [9, 10, 11, 12], [13, 14, 15, 16]]).det(iszerofunc="Not function"))
    raises(ValueError,
        lambda: Matrix([[1, 2, 3, 4], [5, 6, 7, 8],
        [9, 10, 11, 12], [13, 14, 15, 16]]).det(iszerofunc=False))
    raises(ValueError,
        lambda: hessian(Matrix([[1, 2], [3, 4]]), Matrix([[1, 2], [2, 1]])))
    raises(ValueError, lambda: hessian(Matrix([[1, 2], [3, 4]]), []))
    raises(ValueError, lambda: hessian(Symbol('x')**2, 'a'))
    raises(IndexError, lambda: eye(3)[5, 2])
    raises(IndexError, lambda: eye(3)[2, 5])
    M = Matrix(((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16)))
    raises(ValueError, lambda: M.det('method=LU_decomposition()'))
    V = Matrix([[10, 10, 10]])
    M = Matrix([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
    raises(ValueError, lambda: M.row_insert(4.7, V))
    M = Matrix([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
    raises(ValueError, lambda: M.col_insert(-4.2, V))


def test_errors():
    raises(ValueError, lambda: Matrix([[1, 2], [1]]))
    raises(IndexError, lambda: Matrix([[1, 2]])[1.2, 5])
    raises(IndexError, lambda: Matrix([[1, 2]])[1, 5.2])
    raises(ValueError, lambda: randMatrix(3, c=4, symmetric=True))
    raises(ValueError, lambda: Matrix([1, 2]).reshape(4, 6))
    raises(ShapeError,
        lambda: Matrix([[1, 2], [3, 4]]).copyin_matrix([1, 0], Matrix([1, 2])))
    raises(TypeError, lambda: Matrix([[1, 2], [3, 4]]).copyin_list([0,
           1], set()))
    raises(NonSquareMatrixError, lambda: Matrix([[1, 2, 3], [2, 3, 0]]).inv())
    raises(ShapeError,
        lambda: Matrix(1, 2, [1, 2]).row_join(Matrix([[1, 2], [3, 4]])))
    raises(
        ShapeError, lambda: Matrix([1, 2]).col_join(Matrix([[1, 2], [3, 4]])))
    raises(ShapeError, lambda: Matrix([1]).row_insert(1, Matrix([[1,
           2], [3, 4]])))
    raises(ShapeError, lambda: Matrix([1]).col_insert(1, Matrix([[1,
           2], [3, 4]])))
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).trace())
    raises(TypeError, lambda: Matrix([1]).applyfunc(1))
    raises(ValueError, lambda: Matrix([[1, 2], [3, 4]]).minor(4, 5))
    raises(ValueError, lambda: Matrix([[1, 2], [3, 4]]).minor_submatrix(4, 5))
    raises(TypeError, lambda: Matrix([1, 2, 3]).cross(1))
    raises(TypeError, lambda: Matrix([1, 2, 3]).dot(1))
    raises(ShapeError, lambda: Matrix([1, 2, 3]).dot(Matrix([1, 2])))
    raises(ShapeError, lambda: Matrix([1, 2]).dot([]))
    raises(TypeError, lambda: Matrix([1, 2]).dot('a'))
    raises(ShapeError, lambda: Matrix([1, 2]).dot([1, 2, 3]))
    raises(NonSquareMatrixError, lambda: Matrix([1, 2, 3]).exp())
    raises(ShapeError, lambda: Matrix([[1, 2], [3, 4]]).normalized())
    raises(ValueError, lambda: Matrix([1, 2]).inv(method='not a method'))
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).inverse_GE())
    raises(ValueError, lambda: Matrix([[1, 2], [1, 2]]).inverse_GE())
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).inverse_ADJ())
    raises(ValueError, lambda: Matrix([[1, 2], [1, 2]]).inverse_ADJ())
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).inverse_LU())
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).is_nilpotent())
    raises(NonSquareMatrixError, lambda: Matrix([1, 2]).det())
    raises(ValueError,
        lambda: Matrix([[1, 2], [3, 4]]).det(method='Not a real method'))
    raises(ValueError,
        lambda: Matrix([[1, 2, 3, 4], [5, 6, 7, 8],
        [9, 10, 11, 12], [13, 14, 15, 16]]).det(iszerofunc="Not function"))
    raises(ValueError,
        lambda: Matrix([[1, 2, 3, 4], [5, 6, 7, 8],
        [9, 10, 11, 12], [13, 14, 15, 16]]).det(iszerofunc=False))
    raises(ValueError,
        lambda: hessian(Matrix([[1, 2], [3, 4]]), Matrix([[1, 2], [2, 1]])))
    raises(ValueError, lambda: hessian(Matrix([[1, 2], [3, 4]]), []))
    raises(ValueError, lambda: hessian(Symbol('x')**2, 'a'))
    raises(IndexError, lambda: eye(3)[5, 2])
    raises(IndexError, lambda: eye(3)[2, 5])
    M = Matrix(((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 16)))
    raises(ValueError, lambda: M.det('method=LU_decomposition()'))
    V = Matrix([[10, 10, 10]])
    M = Matrix([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
    raises(ValueError, lambda: M.row_insert(4.7, V))
    M = Matrix([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
    raises(ValueError, lambda: M.col_insert(-4.2, V))


def test_errors():
    raises(ShapeError, lambda: Matrix([1]).LUsolve(Matrix([[1, 2], [3, 4]])))


def test_errors():
    raises(ValueError, lambda: SparseMatrix(1.4, 2, lambda i, j: 0))
    raises(TypeError, lambda: SparseMatrix([1, 2, 3], [1, 2]))
    raises(ValueError, lambda: SparseMatrix([[1, 2], [3, 4]])[(1, 2, 3)])
    raises(IndexError, lambda: SparseMatrix([[1, 2], [3, 4]])[5])
    raises(ValueError, lambda: SparseMatrix([[1, 2], [3, 4]])[1, 2, 3])
    raises(TypeError,
        lambda: SparseMatrix([[1, 2], [3, 4]]).copyin_list([0, 1], set()))
    raises(
        IndexError, lambda: SparseMatrix([[1, 2], [3, 4]])[1, 2])
    raises(TypeError, lambda: SparseMatrix([1, 2, 3]).cross(1))
    raises(IndexError, lambda: SparseMatrix(1, 2, [1, 2])[3])
    raises(ShapeError,
        lambda: SparseMatrix(1, 2, [1, 2]) + SparseMatrix(2, 1, [2, 1]))


def test_errors():
    raises(IndexError, lambda: Identity(2)[1, 2, 3, 4, 5])
    raises(IndexError, lambda: Identity(2)[[1, 2, 3, 4, 5]])

