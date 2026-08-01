
def test_raises_on_csc_input():
    with pytest.raises(TypeError):
        graph = csc_array([[0, 1], [0, 0]])
        maximum_flow(graph, 0, 1)
        maximum_flow(graph, 0, 1, method='edmonds_karp')

