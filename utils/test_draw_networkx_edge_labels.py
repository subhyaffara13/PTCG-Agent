
def test_draw_networkx_edge_labels(subplots, tmp_path):
    fig, _ = subplots
    edge = (0, 1)
    G = nx.DiGraph([edge])
    pos = {n: (n, n) for n in G}
    nx.draw(G, pos=pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={edge: "edge"})
    fig.savefig(tmp_path / "test.ps")

