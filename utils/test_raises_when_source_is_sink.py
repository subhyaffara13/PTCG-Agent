
def test_raises_when_source_is_sink():
    with pytest.raises(ValueError):
        graph = csr_array([[0, 1], [0, 0]])
        maximum_flow(graph, 0, 0)
        maximum_flow(graph, 0, 0, method='edmonds_karp')

