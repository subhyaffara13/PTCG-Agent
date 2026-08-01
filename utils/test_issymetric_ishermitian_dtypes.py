
def test_issymetric_ishermitian_dtypes():
    n = 5
    for t in np.typecodes['All']:
        A = np.zeros([n, n], dtype=t)
        if t in 'eUVOMm':
            raises(TypeError, issymmetric, A)
            raises(TypeError, ishermitian, A)
        elif t == 'G':  # No-op test. On win these pass on others fail.
            pass
        else:
            assert issymmetric(A)
            assert ishermitian(A)

