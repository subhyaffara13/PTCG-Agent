
def test_draw_bipartite(subplots, tmp_path):
    fig, _ = subplots
    G = nx.complete_bipartite_graph(2, 5)
    nx.draw_bipartite(G)
    fig.savefig(tmp_path / "test.ps")

