
def test_implemented_error():
    # Attempts to save an unsupported type and checks that an
    # NotImplementedError is raised.

    x = dok_matrix((2,3))
    x[0,1] = 1

    assert_raises(NotImplementedError, save_npz, 'x.npz', x)

