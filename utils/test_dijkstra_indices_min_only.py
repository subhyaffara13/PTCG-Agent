
def test_dijkstra_indices_min_only(directed, SP_ans, indices):
    SP_ans = np.array(SP_ans)
    indices = np.array(indices, dtype=np.int64)
    min_ind_ans = indices[np.argmin(SP_ans[indices, :], axis=0)]
    min_d_ans = np.zeros(SP_ans.shape[0], SP_ans.dtype)
    for k in range(SP_ans.shape[0]):
        min_d_ans[k] = SP_ans[min_ind_ans[k], k]
    min_ind_ans[np.isinf(min_d_ans)] = -9999

    SP, pred, sources = dijkstra(directed_G,
                                 directed=directed,
                                 indices=indices,
                                 min_only=True,
                                 return_predecessors=True)
    assert_array_almost_equal(SP, min_d_ans)
    assert_array_equal(min_ind_ans, sources)
    SP = dijkstra(directed_G,
                  directed=directed,
                  indices=indices,
                  min_only=True,
                  return_predecessors=False)
    assert_array_almost_equal(SP, min_d_ans)

