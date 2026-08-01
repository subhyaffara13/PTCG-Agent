
def test_sparse_in_struct():
    # reproduces bug found by DC where Cython code was insisting on
    # ndarray return type, but getting sparse matrix
    st = {'sparsefield': eye_array(4)}
    stream = BytesIO()
    savemat(stream, {'a':st})
    d = loadmat(stream, struct_as_record=True)
    assert_array_equal(d['a'][0, 0]['sparsefield'].toarray(), np.eye(4))

