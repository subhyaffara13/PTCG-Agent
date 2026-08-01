
def test_individualized_edge_attributes(subplots):
    G = nx.karate_club_graph()
    fig, ax = subplots
    arrowstyles = ["-|>" if (u + v) % 2 == 0 else "-[" for u, v in G.edges()]
    arrowsizes = [10 * (u % 2 + v % 2) + 10 for u, v in G.edges()]
    nx.draw(G, ax=ax, arrows=True, arrowstyle=arrowstyles, arrowsize=arrowsizes)
    arrows = [
        f for f in ax.get_children() if isinstance(f, mpl.patches.FancyArrowPatch)
    ]
    for e, a in zip(G.edges(), arrows):
        assert a.get_mutation_scale() == 10 * (e[0] % 2 + e[1] % 2) + 10
        expected = (
            mpl.patches.ArrowStyle.BracketB
            if sum(e) % 2
            else mpl.patches.ArrowStyle.CurveFilledB
        )
        assert isinstance(a.get_arrowstyle(), expected)

