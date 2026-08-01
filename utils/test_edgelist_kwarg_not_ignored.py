
def test_edgelist_kwarg_not_ignored(subplots):
    # See gh-4994
    G = nx.path_graph(3)
    G.add_edge(0, 0)
    fig, ax = subplots
    nx.draw(G, edgelist=[(0, 1), (1, 2)], ax=ax)  # Exclude self-loop from edgelist
    assert not ax.patches

