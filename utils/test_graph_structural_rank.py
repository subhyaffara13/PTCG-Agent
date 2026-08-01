
def test_graph_structural_rank():
    # Test square matrix #1
    A = csc_array([[1, 1, 0],
                   [1, 0, 1],
                   [0, 1, 0]])
    assert_equal(structural_rank(A), 3)

    # Test square matrix #2
    rows = np.array([0,0,0,0,0,1,1,2,2,3,3,3,3,3,3,4,4,5,5,6,6,7,7])
    cols = np.array([0,1,2,3,4,2,5,2,6,0,1,3,5,6,7,4,5,5,6,2,6,2,4])
    data = np.ones_like(rows)
    B = coo_array((data,(rows,cols)), shape=(8,8))
    assert_equal(structural_rank(B), 6)

    #Test non-square matrix
    C = csc_array([[1, 0, 2, 0],
                   [2, 0, 4, 0]])
    assert_equal(structural_rank(C), 2)

    #Test tall matrix
    assert_equal(structural_rank(C.T), 2)

