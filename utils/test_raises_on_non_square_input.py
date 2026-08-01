
def test_raises_on_non_square_input():
    with pytest.raises(ValueError):
        graph = csr_array([[0, 1, 2], [2, 1, 0]])
        maximum_flow(graph, 0, 1)

