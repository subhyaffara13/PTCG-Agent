
def test_edmonds1_minbranch():
    # Using -G_array and min should give the same as optimal_arborescence_1,
    # but with all edges negative.
    edges = [(u, v, -w) for (u, v, w) in optimal_arborescence_1]

    G = nx.from_numpy_array(-G_array, create_using=nx.DiGraph)

    # Quickly make sure max branching is empty.
    x = branchings.maximum_branching(G)
    x_ = build_branching([])
    assert_equal_branchings(x, x_)

    # Now test the min branching.
    x = branchings.minimum_branching(G)
    x_ = build_branching(edges)
    assert_equal_branchings(x, x_)

