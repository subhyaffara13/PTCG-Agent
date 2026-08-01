
def test_explicit_zero_causes_warning():
    biadjacency = csr_array(((2, 0, 3), (0, 1, 1), (0, 2, 3)))
    with pytest.warns(UserWarning):
        min_weight_full_bipartite_matching(biadjacency)
    with pytest.warns(UserWarning):
        min_weight_full_bipartite_matching(biadjacency.tocoo())

