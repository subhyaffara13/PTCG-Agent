
def test_two_methods_give_same_result_on_many_sparse_inputs():
    # As opposed to the test above, here we do not spell out the expected
    # output; only assert that the two methods give the same result.
    # Concretely, the below tests 100 cases of size 100x100, out of which
    # 36 are infeasible.
    rng = np.random.default_rng(12342309)
    for _ in range(100):
        lsa_raises = False
        mwfbm_raises = False
        sparse = random_array((100, 100), density=0.06,
            data_sampler=lambda size: rng.integers(1, 100, size))
        # In csgraph, zeros correspond to missing edges, so we explicitly
        # replace those with infinities
        dense = np.full(sparse.shape, np.inf)
        dense[sparse.row, sparse.col] = sparse.data
        sparse = sparse.tocsr()
        try:
            row_ind, col_ind = linear_sum_assignment(dense)
            lsa_cost = dense[row_ind, col_ind].sum()
        except ValueError:
            lsa_raises = True
        try:
            row_ind, col_ind = min_weight_full_bipartite_matching(sparse)
            mwfbm_cost = sparse[row_ind, col_ind].sum()
        except ValueError:
            mwfbm_raises = True
        # Ensure that if one method raises, so does the other one.
        assert lsa_raises == mwfbm_raises
        if not lsa_raises:
            assert lsa_cost == mwfbm_cost

