
def test_steiner_tree_non_terminal_leaves_multigraph_self_loop_edges():
    # To verify that the last step of the steiner tree approximation
    # behaves in the case where a non-terminal leaf has a self loop edge
    G = nx.MultiGraph()
    G.add_edges_from([(i, i + 1) for i in range(10)])
    G.add_edges_from([(2, 2), (3, 3), (4, 4), (4, 4), (7, 7)])

    # Remove non-terminal leaves
    _remove_nonterminal_leaves(G, [4, 5, 6, 7])

    # Only the terminal nodes should be left
    assert list(G) == [4, 5, 6, 7]

