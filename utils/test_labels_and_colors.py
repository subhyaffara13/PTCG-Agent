
def test_labels_and_colors():
    G = nx.cubical_graph()
    pos = nx.spring_layout(G, seed=42)  # positions for all nodes
    # nodes
    nx.draw_networkx_nodes(
        G, pos, nodelist=[0, 1, 2, 3], node_color="r", node_size=500, alpha=0.75
    )
    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=[4, 5, 6, 7],
        node_color="b",
        node_size=500,
        alpha=[0.25, 0.5, 0.75, 1.0],
    )
    # edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(0, 1), (1, 2), (2, 3), (3, 0)],
        width=8,
        alpha=0.5,
        edge_color="r",
    )
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
        width=8,
        alpha=0.5,
        edge_color="b",
    )
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=[(4, 5), (5, 6), (6, 7), (7, 4)],
        arrows=True,
        min_source_margin=0.5,
        min_target_margin=0.75,
        width=8,
        edge_color="b",
    )
    # some math labels
    labels = {}
    labels[0] = r"$a$"
    labels[1] = r"$b$"
    labels[2] = r"$c$"
    labels[3] = r"$d$"
    labels[4] = r"$\alpha$"
    labels[5] = r"$\beta$"
    labels[6] = r"$\gamma$"
    labels[7] = r"$\delta$"
    colors = {n: "k" if n % 2 == 0 else "r" for n in range(8)}
    nx.draw_networkx_labels(G, pos, labels, font_size=16)
    nx.draw_networkx_labels(G, pos, labels, font_size=16, font_color=colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=None, rotate=False)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(4, 5): "4-5"})

