
def test_display_edge_margins(node_shape):
    """
    Test that there is a wider gap between the node and the start of an
    incident edge when min_source_margin is specified.

    This test checks that the use os min_{source/target}_margin edge
    attributes result is shorter (more padding) between the edges and
    source and target nodes.


    As a crude visual example, let 's' and 't' represent source and target
    nodes, respectively:

       Default:
       s-----------------------------t

       With margins:
       s   -----------------------   t

    """
    ax = plt.figure().add_subplot(111)
    G = nx.DiGraph([(0, 1)])
    nx.set_node_attributes(G, {0: (0, 0), 1: (1, 1)}, "pos")
    # Get the default patches from the regular visualization
    nx.display(G, canvas=ax, node_shape=node_shape)
    default_arrow = [
        f for f in ax.get_children() if isinstance(f, mpl.patches.FancyArrowPatch)
    ][0]
    default_extent = default_arrow.get_extents().corners()[::2, 0]
    # Now plot again with margins
    ax = plt.figure().add_subplot(111)
    nx.display(
        G,
        canvas=ax,
        edge_source_margin=100,
        edge_target_margin=100,
        node_shape=node_shape,
    )
    padded_arrow = [
        f for f in ax.get_children() if isinstance(f, mpl.patches.FancyArrowPatch)
    ][0]
    padded_extent = padded_arrow.get_extents().corners()[::2, 0]

    # With padding, the left-most extent of the edge should be further to the right
    assert padded_extent[0] > default_extent[0]
    # And the rightmost extent of the edge, further to the left
    assert padded_extent[1] < default_extent[1]
    plt.close()

