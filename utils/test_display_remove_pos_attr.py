
def test_display_remove_pos_attr():
    """
    If the pos attribute isn't provided or is a function, display computes the layout
    and adds it to the graph. We need to ensure that this new attribute is removed from
    the returned graph.
    """
    G = nx.karate_club_graph()
    nx.display(G)
    assert nx.get_node_attributes(G, "display's position attribute name") == {}

