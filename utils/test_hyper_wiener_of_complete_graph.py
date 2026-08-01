
def test_hyper_wiener_of_complete_graph():
    # In a complete graph K_n, the distance is always 1.
    # For K_n, this term is always (1 + 1^2) = 2.
    #
    # The number of ordered pairs is n * (n - 1).
    # The total sum before division is (n * (n - 1)) * 2.
    # The final result is therefore ((n * (n - 1)) * 2) / 2, which
    # simplifies to n * (n - 1).
    n = 5
    G = nx.complete_graph(n)
    assert nx.hyper_wiener_index(G) == n * (n - 1)

