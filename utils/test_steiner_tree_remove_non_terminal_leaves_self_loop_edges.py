
def test_steiner_tree_remove_non_terminal_leaves_self_loop_edges():
    # To verify that the last step of the steiner tree approximation
    # behaves in the case where a non-terminal leaf has a self loop edge
    G = nx.path_graph(10)

    # Add self loops to the terminal nodes
    G.add_edges_from([(2, 2), (3, 3), (4, 4), (7, 7), (8, 8)])

    # Remove non-terminal leaves
    _remove_nonterminal_leaves(G, [4, 5, 6, 7])

    # The terminal nodes should be left
    assert list(G) == [4, 5, 6, 7]  # only the terminal nodes are left

