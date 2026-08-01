
def faux_inf_example():
    """Base test graph for probing faux_infinity bound. See gh-7562"""
    G = nx.DiGraph()

    # Add nodes with demands
    G.add_node("s0", demand=-4)
    G.add_node("s1", demand=-4)
    G.add_node("ns", demand=0)
    G.add_node("nc", demand=0)
    G.add_node("c0", demand=4)
    G.add_node("c1", demand=4)

    # Uniformly weighted edges
    G.add_edge("s0", "ns", weight=1)
    G.add_edge("s1", "ns", weight=1)
    G.add_edge("ns", "nc", weight=1)
    G.add_edge("nc", "c0", weight=1)
    G.add_edge("nc", "c1", weight=1)

    return G

