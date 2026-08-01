
def test_display_labels_and_colors():
    """See 'Labels and Colors' gallery example"""
    fig, ax = plt.subplots()
    G = nx.cubical_graph()
    pos = nx.spring_layout(G, seed=3113794652)  # positions for all nodes
    nx.set_node_attributes(G, pos, "pos")  # Will not be needed after PR 7571
    labels = iter(
        [
            r"$a$",
            r"$b$",
            r"$c$",
            r"$d$",
            r"$\alpha$",
            r"$\beta$",
            r"$\gamma$",
            r"$\delta$",
        ]
    )
    nx.set_node_attributes(
        G,
        {
            n: {
                "size": 800,
                "alpha": 0.9,
                "color": "tab:red" if n < 4 else "tab:blue",
                "label": {"label": next(labels), "size": 22, "color": "whitesmoke"},
            }
            for n in G.nodes()
        },
    )

    nx.display(G, node_pos="pos", edge_color="tab:grey")

    # The tricky bit is the highlighted colors for the edges
    edgelist = [(0, 1), (1, 2), (2, 3), (0, 3)]
    nx.set_edge_attributes(
        G,
        {
            (u, v): {
                "width": 8,
                "alpha": 0.5,
                "color": "tab:red",
                "visible": (u, v) in edgelist,
            }
            for u, v in G.edges()
        },
    )
    nx.display(G, node_pos="pos", node_visible=False)
    edgelist = [(4, 5), (5, 6), (6, 7), (4, 7)]
    nx.set_edge_attributes(
        G,
        {
            (u, v): {
                "color": "tab:blue",
                "visible": (u, v) in edgelist,
            }
            for u, v in G.edges()
        },
    )
    nx.display(G, node_pos="pos", node_visible=False)

    plt.tight_layout()
    plt.axis("off")
    return fig

