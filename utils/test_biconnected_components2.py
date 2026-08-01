
def test_biconnected_components2():
    G = nx.Graph()
    nx.add_cycle(G, "ABC")
    nx.add_cycle(G, "CDE")
    nx.add_cycle(G, "FIJHG")
    nx.add_cycle(G, "GIJ")
    G.add_edge("E", "G")
    comps = list(nx.biconnected_component_edges(G))
    answer = [
        [
            tuple("GF"),
            tuple("FI"),
            tuple("IG"),
            tuple("IJ"),
            tuple("JG"),
            tuple("JH"),
            tuple("HG"),
        ],
        [tuple("EG")],
        [tuple("CD"), tuple("DE"), tuple("CE")],
        [tuple("AB"), tuple("BC"), tuple("AC")],
    ]
    assert_components_edges_equal(comps, answer)

