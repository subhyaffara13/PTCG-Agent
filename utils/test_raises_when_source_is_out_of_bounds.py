
def test_raises_when_source_is_out_of_bounds(source, method):
    with pytest.raises(ValueError):
        graph = csr_array([[0, 1], [0, 0]])
        maximum_flow(graph, source, 1, method=method)

