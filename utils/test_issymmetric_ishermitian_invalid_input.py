
def test_issymmetric_ishermitian_invalid_input():
    A = np.array([1, 2, 3])
    raises(ValueError, issymmetric, A)
    raises(ValueError, ishermitian, A)
    A = np.array([[[1, 2, 3], [4, 5, 6]]])
    raises(ValueError, issymmetric, A)
    raises(ValueError, ishermitian, A)
    A = np.array([[1, 2, 3], [4, 5, 6]])
    raises(ValueError, issymmetric, A)
    raises(ValueError, ishermitian, A)

