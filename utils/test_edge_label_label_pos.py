
def test_edge_label_label_pos(subplots, label_pos):
    """
    Check that label positions can be extrapolated outside [0, 1].
    """
    fig, ax = subplots
    edge = (0, 1)
    G = nx.DiGraph([edge])
    pos = {n: (n, n) for n in G}
    lbl = nx.draw_networkx_edge_labels(
        G, pos, edge_labels={edge: "edge"}, label_pos=label_pos, connectionstyle="angle"
    )

    assert lbl[edge].x, lbl[edge].y == pytest.approx((label_pos, label_pos))

