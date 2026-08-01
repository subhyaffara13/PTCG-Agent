
def test_3d_coo_singleton(scalar_container):
    A[(0, 0, 0)] = scalar_container(-99)
    D[(0, 0, 0)] = -99
    assert_equal(A.toarray(), D)

