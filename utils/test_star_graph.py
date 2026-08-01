
def test_star_graph(n, method, directed):
    # Build the star graph
    star_arr = np.zeros((n, n), dtype=float)
    star_center_idx = 0
    star_arr[star_center_idx, :] = star_arr[:, star_center_idx] = range(n)
    G = scipy.sparse.csr_array(star_arr, shape=(n, n))
    # Build the distances matrix
    SP_solution = np.zeros((n, n), dtype=float)
    SP_solution[:] = star_arr[star_center_idx]
    for idx in range(1, n):
        SP_solution[idx] += star_arr[idx, star_center_idx]
    np.fill_diagonal(SP_solution, 0)

    SP = shortest_path(G, method=method, directed=directed)
    assert_allclose(
        SP_solution, SP
    )


def test_star_graph():
    G = nx.star_graph(3)
    # all modes are the same
    answer = {0: 0, 1: 1, 2: 1, 3: 1}
    assert bipartite.clustering(G, mode="dot") == answer
    assert bipartite.clustering(G, mode="min") == answer
    assert bipartite.clustering(G, mode="max") == answer

