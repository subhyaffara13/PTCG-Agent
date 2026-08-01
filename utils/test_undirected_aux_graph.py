
def test_undirected_aux_graph():
    # Graph similar to the one in
    # http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0136264
    a, b, c, d, e, f, g, h, i = "abcdefghi"
    paths = [
        (a, d, b, f, c),
        (a, e, b),
        (a, e, b, c, g, b, a),
        (c, b),
        (f, g, f),
        (h, i),
    ]
    G = nx.Graph(it.chain(*[pairwise(path) for path in paths]))
    aux_graph = EdgeComponentAuxGraph.construct(G)

    components_1 = fset(aux_graph.k_edge_subgraphs(k=1))
    target_1 = fset([{a, b, c, d, e, f, g}, {h, i}])
    assert target_1 == components_1

    # Check that the undirected case for k=1 agrees with CCs
    alt_1 = fset(nx.k_edge_subgraphs(G, k=1))
    assert alt_1 == components_1

    components_2 = fset(aux_graph.k_edge_subgraphs(k=2))
    target_2 = fset([{a, b, c, d, e, f, g}, {h}, {i}])
    assert target_2 == components_2

    # Check that the undirected case for k=2 agrees with bridge components
    alt_2 = fset(nx.k_edge_subgraphs(G, k=2))
    assert alt_2 == components_2

    components_3 = fset(aux_graph.k_edge_subgraphs(k=3))
    target_3 = fset([{a}, {b, c, f, g}, {d}, {e}, {h}, {i}])
    assert target_3 == components_3

    components_4 = fset(aux_graph.k_edge_subgraphs(k=4))
    target_4 = fset([{a}, {b}, {c}, {d}, {e}, {f}, {g}, {h}, {i}])
    assert target_4 == components_4

    _check_edge_connectivity(G)

