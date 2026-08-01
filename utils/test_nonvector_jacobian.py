
def test_nonvectorJacobian():
    X = Matrix([[exp(x + y + z), exp(x + y + z)],
                [exp(x + y + z), exp(x + y + z)]])
    raises(TypeError, lambda: _forward_jacobian(X, Matrix([x, y, z])))
    X = X[0, :]
    Y = Matrix([[x, y], [x, z]])
    raises(TypeError, lambda: _forward_jacobian(X, Y))
    raises(TypeError, lambda: _forward_jacobian(X, Matrix([[x, y], [x, z]])))


def test_nonvectorJacobian():
    X = Matrix([[exp(x + y + z), exp(x + y + z)],
                [exp(x + y + z), exp(x + y + z)]])
    raises(TypeError, lambda: X.jacobian(Matrix([x, y, z])))
    X = X[0, :]
    Y = Matrix([[x, y], [x, z]])
    raises(TypeError, lambda: X.jacobian(Y))
    raises(TypeError, lambda: X.jacobian(Matrix([ [x, y], [x, z] ])))


def test_nonvectorJacobian():
    X = Matrix([[exp(x + y + z), exp(x + y + z)],
                [exp(x + y + z), exp(x + y + z)]])
    raises(TypeError, lambda: X.jacobian(Matrix([x, y, z])))
    X = X[0, :]
    Y = Matrix([[x, y], [x, z]])
    raises(TypeError, lambda: X.jacobian(Y))
    raises(TypeError, lambda: X.jacobian(Matrix([ [x, y], [x, z] ])))

