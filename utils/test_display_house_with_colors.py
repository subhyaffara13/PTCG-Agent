
def test_display_house_with_colors():
    """
    Originally, I wanted to use the exact samge image as test_house_with_colors.
    But I can't seem to find the correct value for the margins to get the figures
    to line up perfectly. To the human eye, these visualizations are basically the
    same.
    """
    G = nx.house_graph()
    fig, ax = plt.subplots()
    nx.set_node_attributes(
        G, {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1), 4: (0.5, 2.0)}, "pos"
    )
    nx.set_node_attributes(
        G,
        {
            n: {
                "size": 3000 if n != 4 else 2000,
                "color": "tab:blue" if n != 4 else "tab:orange",
            }
            for n in G.nodes()
        },
    )
    nx.display(
        G,
        node_pos="pos",
        edge_alpha=0.5,
        edge_width=6,
        node_label=None,
        node_border_color="k",
    )
    ax.margins(0.17)
    plt.tight_layout()
    plt.axis("off")
    return fig

