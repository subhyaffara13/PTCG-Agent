
def test_issymetric_complex_decimals():
    A = np.arange(1, 10).astype(complex).reshape(3, 3)
    A += np.arange(-4, 5).astype(complex).reshape(3, 3)*1j
    # make entries decimal
    A /= np.pi
    A = A + A.T
    assert issymmetric(A)

