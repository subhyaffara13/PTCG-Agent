
def test_matching_large_random_graph_with_one_edge_incident_to_each_vertex():
    np.random.seed(42)
    A = diags_array(np.ones(25), offsets=0, format='csr')
    rand_perm = np.random.permutation(25)
    rand_perm2 = np.random.permutation(25)

    Rrow = np.arange(25)
    Rcol = rand_perm
    Rdata = np.ones(25, dtype=int)
    Rmat = csr_array((Rdata, (Rrow, Rcol)))

    Crow = rand_perm2
    Ccol = np.arange(25)
    Cdata = np.ones(25, dtype=int)
    Cmat = csr_array((Cdata, (Crow, Ccol)))
    # Randomly permute identity matrix
    B = Rmat @ A @ Cmat

    # Row permute
    perm = maximum_bipartite_matching(B, perm_type='row')
    Rrow = np.arange(25)
    Rcol = perm
    Rdata = np.ones(25, dtype=int)
    Rmat = csr_array((Rdata, (Rrow, Rcol)))
    C1 = Rmat @ B

    # Column permute
    perm2 = maximum_bipartite_matching(B, perm_type='column')
    Crow = perm2
    Ccol = np.arange(25)
    Cdata = np.ones(25, dtype=int)
    Cmat = csr_array((Cdata, (Crow, Ccol)))
    C2 = B @ Cmat

    # Should get identity matrix back
    assert_equal(any(C1.diagonal() == 0), False)
    assert_equal(any(C2.diagonal() == 0), False)

