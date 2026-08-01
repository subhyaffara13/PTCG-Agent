
def test_LinearVectorFunctionNoReferenceCycle():
    """Regression test for gh-20768."""
    A_dense = np.array([
        [-1, 2, 0],
        [0, 4, 2]
    ])
    x0 = np.zeros(3)
    A_sparse = csr_array(A_dense)
    with assert_deallocated(lambda: LinearVectorFunction(A_sparse, x0, None)):
        pass

