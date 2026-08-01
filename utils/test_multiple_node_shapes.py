
def test_multiple_node_shapes(subplots):
    fig, ax = subplots
    G = nx.path_graph(4)
    nx.draw(G, node_shape=["o", "h", "s", "^"], ax=ax)
    scatters = [
        s for s in ax.get_children() if isinstance(s, mpl.collections.PathCollection)
    ]
    assert len(scatters) == 4

