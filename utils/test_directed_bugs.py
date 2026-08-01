
def test_directed_bugs():
    """
    These were bugs for directed graphs as discussed in issue #7806
    """
    Ga = nx.DiGraph()
    Gb = nx.DiGraph()
    Ga.add_nodes_from([1, 2, 3, 4])
    Gb.add_nodes_from([1, 2, 3, 4])
    Ga.add_edges_from([(1, 2), (3, 2)])
    Gb.add_edges_from([(1, 2), (3, 4)])
    Ga_hash = nx.weisfeiler_lehman_graph_hash(Ga)
    Gb_hash = nx.weisfeiler_lehman_graph_hash(Gb)
    assert Ga_hash != Gb_hash

    Tree1 = nx.DiGraph()
    Tree1.add_edges_from([(0, 4), (1, 5), (2, 6), (3, 7)])
    Tree1.add_edges_from([(4, 8), (5, 8), (6, 9), (7, 9)])
    Tree1.add_edges_from([(8, 10), (9, 10)])
    nx.set_node_attributes(
        Tree1, {10: "s", 8: "a", 9: "a", 4: "b", 5: "b", 6: "b", 7: "b"}, "weight"
    )
    Tree2 = copy.deepcopy(Tree1)
    nx.set_node_attributes(Tree1, {0: "d", 1: "c", 2: "d", 3: "c"}, "weight")
    nx.set_node_attributes(Tree2, {0: "d", 1: "d", 2: "c", 3: "c"}, "weight")
    Tree1_hash_short = nx.weisfeiler_lehman_graph_hash(
        Tree1, iterations=1, node_attr="weight"
    )
    Tree2_hash_short = nx.weisfeiler_lehman_graph_hash(
        Tree2, iterations=1, node_attr="weight"
    )
    assert Tree1_hash_short == Tree2_hash_short
    Tree1_hash = nx.weisfeiler_lehman_graph_hash(
        Tree1, node_attr="weight"
    )  # Default is 3 iterations
    Tree2_hash = nx.weisfeiler_lehman_graph_hash(Tree2, node_attr="weight")
    assert Tree1_hash != Tree2_hash

