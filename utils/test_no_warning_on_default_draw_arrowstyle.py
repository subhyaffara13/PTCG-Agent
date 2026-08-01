
def test_no_warning_on_default_draw_arrowstyle(draw_fn, subplots):
    # See gh-7284
    fig, ax = subplots
    G = nx.cycle_graph(5)
    with warnings.catch_warnings(record=True) as w:
        draw_fn(G, ax=ax)
    assert len(w) == 0

