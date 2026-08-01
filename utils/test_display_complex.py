
def test_display_complex():
    import itertools as it

    fig, ax = plt.subplots()
    G = nx.MultiDiGraph()
    nodes = "ABC"
    prod = list(it.product(nodes, repeat=2)) * 4
    G = nx.MultiDiGraph()
    for i, (u, v) in enumerate(prod):
        G.add_edge(u, v, w=round(i / 3, 2))
    nx.set_node_attributes(G, nx.spring_layout(G, seed=3113794652), "pos")
    csi = it.cycle([f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)])
    nx.set_edge_attributes(G, {e: next(csi) for e in G.edges(keys=True)}, "curvature")
    nx.set_edge_attributes(
        G,
        {
            tuple(e): {"label": w, "bbox": {"alpha": 0}}
            for *e, w in G.edges(keys=True, data="w")
        },
        "label",
    )
    nx.apply_matplotlib_colors(G, "w", "color", mpl.colormaps["inferno"], nodes=False)
    nx.display(G, canvas=ax, node_pos="pos")

    plt.tight_layout()
    plt.axis("off")
    return fig

