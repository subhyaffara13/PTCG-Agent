
def test_matrix_derivative_trivial_cases():
    # Cookbook example 33:
    # TODO: find a way to represent a four-dimensional zero-array:
    assert X.diff(A) == ArrayDerivative(X, A)

