
def test_transshipment():
    G = nx.DiGraph()
    G.add_node("a", demand=1)
    G.add_node("b", demand=-2)
    G.add_node("c", demand=-2)
    G.add_node("d", demand=3)
    G.add_node("e", demand=-4)
    G.add_node("f", demand=-4)
    G.add_node("g", demand=3)
    G.add_node("h", demand=2)
    G.add_node("r", demand=3)
    G.add_edge("a", "c", weight=3)
    G.add_edge("r", "a", weight=2)
    G.add_edge("b", "a", weight=9)
    G.add_edge("r", "c", weight=0)
    G.add_edge("b", "r", weight=-6)
    G.add_edge("c", "d", weight=5)
    G.add_edge("e", "r", weight=4)
    G.add_edge("e", "f", weight=3)
    G.add_edge("h", "b", weight=4)
    G.add_edge("f", "d", weight=7)
    G.add_edge("f", "h", weight=12)
    G.add_edge("g", "d", weight=12)
    G.add_edge("f", "g", weight=-1)
    G.add_edge("h", "g", weight=-10)
    flowCost, H = nx.network_simplex(G)
    soln = {
        "a": {"c": 0},
        "b": {"a": 0, "r": 2},
        "c": {"d": 3},
        "d": {},
        "e": {"r": 3, "f": 1},
        "f": {"d": 0, "g": 3, "h": 2},
        "g": {"d": 0},
        "h": {"b": 0, "g": 0},
        "r": {"a": 1, "c": 1},
    }
    assert flowCost == 41
    assert H == soln

