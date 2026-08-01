
def test_gnp_generators_edge_probability(generator, p, directed):
    """Test that gnp generators generate edges according to the their probability `p`."""
    runs = 5000
    n = 5
    edge_counts = [[0] * n for _ in range(n)]
    for i in range(runs):
        G = generator(n, p, directed=directed)
        for v, w in G.edges:
            edge_counts[v][w] += 1
            if not directed:
                edge_counts[w][v] += 1
    for v in range(n):
        for w in range(n):
            if v == w:
                # There should be no loops
                assert edge_counts[v][w] == 0
            else:
                # Each edge should have been generated with probability close to p
                assert abs(edge_counts[v][w] / float(runs) - p) <= 0.03

