
def test_maximum_bipartite_matching_raises_on_dense_input():
    with pytest.raises(TypeError):
        graph = np.array([[0, 1], [0, 0]])
        maximum_bipartite_matching(graph)

