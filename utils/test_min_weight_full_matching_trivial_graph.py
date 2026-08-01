
def test_min_weight_full_matching_trivial_graph(num_rows, num_cols):
    biadjacency = csr_array((num_cols, num_rows))
    biadjacency1 = coo_array((num_cols, num_rows))

    row_ind, col_ind = min_weight_full_bipartite_matching(biadjacency)
    assert len(row_ind) == 0
    assert len(col_ind) == 0

    row_ind1, col_ind1 = min_weight_full_bipartite_matching(biadjacency1)
    assert len(row_ind1) == 0
    assert len(col_ind1) == 0

