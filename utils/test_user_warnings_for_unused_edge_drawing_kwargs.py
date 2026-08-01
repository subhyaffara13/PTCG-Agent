
def test_user_warnings_for_unused_edge_drawing_kwargs(fap_only_kwarg, subplots):
    """Users should get a warning when they specify a non-default value for
    one of the kwargs that applies only to edges drawn with FancyArrowPatches,
    but FancyArrowPatches aren't being used under the hood."""
    G = nx.path_graph(3)
    pos = {n: (n, n) for n in G}
    fig, ax = subplots
    # By default, an undirected graph will use LineCollection to represent
    # the edges
    kwarg_name = list(fap_only_kwarg.keys())[0]
    with pytest.warns(
        UserWarning, match=f"\n\nThe {kwarg_name} keyword argument is not applicable"
    ):
        nx.draw_networkx_edges(G, pos, ax=ax, **fap_only_kwarg)
    # FancyArrowPatches are always used when `arrows=True` is specified.
    # Check that warnings are *not* raised in this case
    with warnings.catch_warnings():
        # Escalate warnings -> errors so tests fail if warnings are raised
        warnings.simplefilter("error")
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        nx.draw_networkx_edges(G, pos, ax=ax, arrows=True, **fap_only_kwarg)

