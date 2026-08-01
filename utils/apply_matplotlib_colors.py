
def apply_matplotlib_colors(
    G, src_attr, dest_attr, map, vmin=None, vmax=None, nodes=True
):
    """
    Apply colors from a matplotlib colormap to a graph.

    Reads values from the `src_attr` and use a matplotlib colormap
    to produce a color. Write the color to `dest_attr`.

    Parameters
    ----------
    G : nx.Graph
        The graph to read and compute colors for.

    src_attr : str or other attribute name
        The name of the attribute to read from the graph.

    dest_attr : str or other attribute name
        The name of the attribute to write to on the graph.

    map : matplotlib.colormap
        The matplotlib colormap to use.

    vmin : float, default None
        The minimum value for scaling the colormap. If `None`, find the
        minimum value of `src_attr`.

    vmax : float, default None
        The maximum value for scaling the colormap. If `None`, find the
        maximum value of `src_attr`.

    nodes : bool, default True
        Whether the attribute names are edge attributes or node attributes.
    """
    import matplotlib as mpl

    if nodes:
        type_iter = G.nodes()
    elif G.is_multigraph():
        type_iter = G.edges(keys=True)
    else:
        type_iter = G.edges()

    if vmin is None or vmax is None:
        vals = [type_iter[a][src_attr] for a in type_iter]
        if vmin is None:
            vmin = min(vals)
        if vmax is None:
            vmax = max(vals)

    mapper = mpl.cm.ScalarMappable(cmap=map)
    mapper.set_clim(vmin, vmax)

    def do_map(x):
        # Cast numpy scalars to float
        return tuple(float(x) for x in mapper.to_rgba(x))

    if nodes:
        nx.set_node_attributes(
            G, {n: do_map(G.nodes[n][src_attr]) for n in G.nodes()}, dest_attr
        )
    else:
        nx.set_edge_attributes(
            G, {e: do_map(G.edges[e][src_attr]) for e in type_iter}, dest_attr
        )

