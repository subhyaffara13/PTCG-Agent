import itertools

def test_draw_edges_arrowstyle(arrowstyle):
    G = nx.DiGraph([(0, 1), (0, 2), (1, 2)])
    pos = {0: (0, 0), 1: (0, 1), 2: (1, 0)}
    edges = nx.draw_networkx_edges(G, pos=pos, arrowstyle=arrowstyle)

    arrowstyle = (
        itertools.repeat(arrowstyle) if isinstance(arrowstyle, str) else arrowstyle
    )

    arrow_objects = {
        "-|>": mpl.patches.ArrowStyle.CurveFilledB,
        "-[": mpl.patches.ArrowStyle.BracketB,
        "<|-|>": mpl.patches.ArrowStyle.CurveFilledAB,
    }

    for fap, expected in zip(edges, arrowstyle):
        assert isinstance(fap, mpl.patches.FancyArrowPatch)
        assert isinstance(fap.get_arrowstyle(), arrow_objects[expected])

