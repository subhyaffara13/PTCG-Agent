
def test_raises_on_floating_point_input():
    with pytest.raises(ValueError):
        graph = csr_array([[0, 1.5], [0, 0]], dtype=np.float64)
        maximum_flow(graph, 0, 1)
        maximum_flow(graph, 0, 1, method='edmonds_karp')

