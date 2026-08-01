
def test_reshape_overflow():
    # see gh-22353 : new idx_dtype can need to be int64 instead of int32
    M, N = (1045507, 523266)
    coords = (np.array([M - 1], dtype='int32'), np.array([N - 1], dtype='int32'))
    A = coo_array(([3.3], coords), shape=(M, N))

    # need new idx_dtype to not overflow
    B = A.reshape((M * N, 1))
    assert B.coords[0].dtype == np.dtype('int64')
    assert B.coords[0][0] == (M * N) - 1

    # need idx_dtype to stay int32 if before and after can be int32
    C = A.reshape(N, M)
    assert C.coords[0].dtype == np.dtype('int32')
    assert C.coords[0][0] == N - 1

