
def test_min_weight_full_matching_infeasible_problems(biadjacency):
    with pytest.raises(ValueError):
        min_weight_full_bipartite_matching(csr_array(biadjacency))
    with pytest.raises(ValueError):
        min_weight_full_bipartite_matching(coo_array(biadjacency))

