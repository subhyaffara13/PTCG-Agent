
def test_edge_label_all_connectionstyles(subplots, style):
    """
    Check that FancyArrowPatches with all `connectionstyle`s are supported
    in edge label rendering. See gh-7735 and gh-8106.
    """
    fig, ax = subplots
    edge = (0, 1)
    G = nx.DiGraph([edge])
    pos = {n: (n, 0) for n in G}

    name = style.split(",")[0]
    labels = nx.draw_networkx_edge_labels(
        G, pos, edge_labels={edge: "edge"}, connectionstyle=style
    )

    hmid = (pos[0][0] + pos[1][0]) / 2
    vmid = (pos[0][1] + pos[1][1]) / 2
    if name in {"arc", "arc3"}:  # The label should be at roughly the midpoint.
        assert labels[edge].x, labels[edge].y == pytest.approx((hmid, vmid))
    elif name == "bar":  # The label should be below the vertical midpoint.
        assert labels[edge].y < vmid

