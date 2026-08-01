
def test_raises_when_sink_is_out_of_bounds(sink, method):
    with pytest.raises(ValueError):
        graph = csr_array([[0, 1], [0, 0]])
        maximum_flow(graph, 0, sink, method=method)

