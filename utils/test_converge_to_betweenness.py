
def test_converge_to_betweenness():
    """percolation centrality: should converge to betweenness
    centrality when all nodes are percolated the same"""
    # taken from betweenness test test_florentine_families_graph
    G = nx.florentine_families_graph()
    b_answer = {
        "Acciaiuoli": 0.000,
        "Albizzi": 0.212,
        "Barbadori": 0.093,
        "Bischeri": 0.104,
        "Castellani": 0.055,
        "Ginori": 0.000,
        "Guadagni": 0.255,
        "Lamberteschi": 0.000,
        "Medici": 0.522,
        "Pazzi": 0.000,
        "Peruzzi": 0.022,
        "Ridolfi": 0.114,
        "Salviati": 0.143,
        "Strozzi": 0.103,
        "Tornabuoni": 0.092,
    }

    # If no initial state is provided, state for
    # every node defaults to 1
    p_answer = nx.percolation_centrality(G)
    assert p_answer == pytest.approx(b_answer, abs=1e-3)

    p_states = {k: 0.3 for k, v in b_answer.items()}
    p_answer = nx.percolation_centrality(G, states=p_states)
    assert p_answer == pytest.approx(b_answer, abs=1e-3)

