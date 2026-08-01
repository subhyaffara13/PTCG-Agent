
def test_construct_dist_matrix_predecessors_error(directed):
    SP1, pred = shortest_path(directed_G,
                                directed=directed,
                                overwrite=False,
                                return_predecessors=True)
    assert_raises(TypeError, construct_dist_matrix,
                  directed_G, pred.astype(np.int64), directed)

