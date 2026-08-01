
def test_draw_edges_min_source_target_margins_individual(node_shape, subplots):
    """Test that there is a wider gap between the node and the start of an
    incident edge when min_source_margin is specified.

    This test checks that the use of min_{source/target}_margin kwargs result
    in shorter (more padding) between the edges and source and target nodes.
    As a crude visual example, let 's' and 't' represent source and target
    nodes, respectively:

       Default:
       s-----------------------------t

       With margins:
       s   -----------------------   t

    """
    # Create a single axis object to get consistent pixel coords across
    # multiple draws
    fig, ax = subplots
    G = nx.DiGraph([(0, 1), (1, 2)])
    pos = {0: (0, 0), 1: (1, 0), 2: (2, 0)}  # horizontal layout
    # Get leftmost and rightmost points of the FancyArrowPatch object
    # representing the edge between nodes 0 and 1 (in pixel coordinates)
    default_patch = nx.draw_networkx_edges(G, pos, ax=ax, node_shape=node_shape)
    default_extent = [d.get_extents().corners()[::2, 0] for d in default_patch]
    # Now, do the same but with "padding" for the source and target via the
    # min_{source/target}_margin kwargs
    padded_patch = nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        node_shape=node_shape,
        min_source_margin=[98, 102],
        min_target_margin=[98, 102],
    )
    padded_extent = [p.get_extents().corners()[::2, 0] for p in padded_patch]
    for d, p in zip(default_extent, padded_extent):
        # With padding, the left-most extent of the edge should be further to the
        # right
        assert p[0] > d[0]
        # And the rightmost extent of the edge, further to the left
        assert p[1] < d[1]

