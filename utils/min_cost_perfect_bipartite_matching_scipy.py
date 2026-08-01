
def min_cost_perfect_bipartite_matching_scipy(G):
    n = len(G)
    rows, cols = linear_sum_assignment(G)
    assert (rows == list(range(n))).all()
    # Convert numpy array and integer to Python types,
    # to ensure that this is JSON-serializable.
    cols = list(int(e) for e in cols)
    return list(cols), matching_cost(G, cols)

