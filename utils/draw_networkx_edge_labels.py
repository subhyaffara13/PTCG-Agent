
def draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=None,
    label_pos=0.5,
    font_size=10,
    font_color="k",
    font_family="sans-serif",
    font_weight="normal",
    alpha=None,
    bbox=None,
    horizontalalignment="center",
    verticalalignment="center",
    ax=None,
    rotate=True,
    clip_on=True,
    node_size=300,
    nodelist=None,
    connectionstyle="arc3",
    hide_ticks=True,
):
    """Draw edge labels.

    Parameters
    ----------
    G : graph
        A networkx graph

    pos : dictionary
        A dictionary with nodes as keys and positions as values.
        Positions should be sequences of length 2.

    edge_labels : dictionary (default=None)
        Edge labels in a dictionary of labels keyed by edge two-tuple.
        Only labels for the keys in the dictionary are drawn.

    label_pos : float (default=0.5)
        Position of edge label along edge (0=head, 0.5=center, 1=tail)

    font_size : int (default=10)
        Font size for text labels

    font_color : color (default='k' black)
        Font color string. Color can be string or rgb (or rgba) tuple of
        floats from 0-1.

    font_weight : string (default='normal')
        Font weight

    font_family : string (default='sans-serif')
        Font family

    alpha : float or None (default=None)
        The text transparency

    bbox : Matplotlib bbox, optional
        Specify text box properties (e.g. shape, color etc.) for edge labels.
        Default is {boxstyle='round', ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0)}.

    horizontalalignment : string (default='center')
        Horizontal alignment {'center', 'right', 'left'}

    verticalalignment : string (default='center')
        Vertical alignment {'center', 'top', 'bottom', 'baseline', 'center_baseline'}

    ax : Matplotlib Axes object, optional
        Draw the graph in the specified Matplotlib axes.

    rotate : bool (default=True)
        Rotate edge labels to lie parallel to edges

    clip_on : bool (default=True)
        Turn on clipping of edge labels at axis boundaries

    node_size : scalar or array (default=300)
        Size of nodes.  If an array it must be the same length as nodelist.

    nodelist : list, optional (default=G.nodes())
       This provides the node order for the `node_size` array (if it is an array).

    connectionstyle : string or iterable of strings (default="arc3")
        Pass the connectionstyle parameter to create curved arc of rounding
        radius rad. For example, connectionstyle='arc3,rad=0.2'.
        See `matplotlib.patches.ConnectionStyle` and
        `matplotlib.patches.FancyArrowPatch` for more info.
        If Iterable, index indicates i'th edge key of MultiGraph

    hide_ticks : bool, optional
        Hide ticks of axes. When `True` (the default), ticks and ticklabels
        are removed from the axes. To set ticks and tick labels to the pyplot default,
        use ``hide_ticks=False``.

    Returns
    -------
    dict
        `dict` of labels keyed by edge

    Examples
    --------
    >>> G = nx.dodecahedral_graph()
    >>> edge_labels = nx.draw_networkx_edge_labels(G, pos=nx.spring_layout(G))

    Also see the NetworkX drawing examples at
    https://networkx.org/documentation/latest/auto_examples/index.html

    See Also
    --------
    draw
    draw_networkx
    draw_networkx_nodes
    draw_networkx_edges
    draw_networkx_labels
    """
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np

    class CurvedArrowText(CurvedArrowTextBase, mpl.text.Text):
        pass

    # use default box of white with white border
    if bbox is None:
        bbox = {"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0)}

    if isinstance(connectionstyle, str):
        connectionstyle = [connectionstyle]
    elif np.iterable(connectionstyle):
        connectionstyle = list(connectionstyle)
    else:
        raise nx.NetworkXError(
            "draw_networkx_edges arg `connectionstyle` must be"
            "string or iterable of strings"
        )

    if ax is None:
        ax = plt.gca()

    if edge_labels is None:
        kwds = {"keys": True} if G.is_multigraph() else {}
        edge_labels = {tuple(edge): d for *edge, d in G.edges(data=True, **kwds)}
    # NOTHING TO PLOT
    if not edge_labels:
        return {}
    edgelist, labels = zip(*edge_labels.items())

    if nodelist is None:
        nodelist = list(G.nodes())

    # set edge positions
    edge_pos = np.asarray([(pos[e[0]], pos[e[1]]) for e in edgelist])

    if G.is_multigraph():
        key_count = collections.defaultdict(lambda: itertools.count(0))
        edge_indices = [next(key_count[tuple(e[:2])]) for e in edgelist]
    else:
        edge_indices = [0] * len(edgelist)

    # Used to determine self loop mid-point
    # Note, that this will not be accurate,
    #   if not drawing edge_labels for all edges drawn
    h = 0
    if edge_labels:
        miny = np.amin(np.ravel(edge_pos[:, :, 1]))
        maxy = np.amax(np.ravel(edge_pos[:, :, 1]))
        h = maxy - miny
    selfloop_height = h if h != 0 else 0.005 * np.array(node_size).max()
    fancy_arrow_factory = FancyArrowFactory(
        edge_pos,
        edgelist,
        nodelist,
        edge_indices,
        node_size,
        selfloop_height,
        connectionstyle,
        ax=ax,
    )

    individual_params = {}

    def check_individual_params(p_value, p_name):
        # TODO should this be list or array (as in a numpy array)?
        if isinstance(p_value, list):
            if len(p_value) != len(edgelist):
                raise ValueError(f"{p_name} must have the same length as edgelist.")
            individual_params[p_name] = p_value.iter()

    # Don't need to pass in an edge because these are lists, not dicts
    def get_param_value(p_value, p_name):
        if p_name in individual_params:
            return next(individual_params[p_name])
        return p_value

    check_individual_params(font_size, "font_size")
    check_individual_params(font_color, "font_color")
    check_individual_params(font_weight, "font_weight")
    check_individual_params(alpha, "alpha")
    check_individual_params(horizontalalignment, "horizontalalignment")
    check_individual_params(verticalalignment, "verticalalignment")
    check_individual_params(rotate, "rotate")
    check_individual_params(label_pos, "label_pos")

    text_items = {}
    for i, (edge, label) in enumerate(zip(edgelist, labels)):
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same

        n1, n2 = edge[:2]
        arrow = fancy_arrow_factory(i)
        if n1 == n2:
            connectionstyle_obj = arrow.get_connectionstyle()
            posA = ax.transData.transform(pos[n1])
            path_disp = connectionstyle_obj(posA, posA)
            path_data = ax.transData.inverted().transform_path(path_disp)
            x, y = path_data.vertices[0]
            text_items[edge] = ax.text(
                x,
                y,
                label,
                size=get_param_value(font_size, "font_size"),
                color=get_param_value(font_color, "font_color"),
                family=get_param_value(font_family, "font_family"),
                weight=get_param_value(font_weight, "font_weight"),
                alpha=get_param_value(alpha, "alpha"),
                horizontalalignment=get_param_value(
                    horizontalalignment, "horizontalalignment"
                ),
                verticalalignment=get_param_value(
                    verticalalignment, "verticalalignment"
                ),
                rotation=0,
                transform=ax.transData,
                bbox=bbox,
                zorder=1,
                clip_on=clip_on,
            )
        else:
            text_items[edge] = CurvedArrowText(
                arrow,
                label,
                size=get_param_value(font_size, "font_size"),
                color=get_param_value(font_color, "font_color"),
                family=get_param_value(font_family, "font_family"),
                weight=get_param_value(font_weight, "font_weight"),
                alpha=get_param_value(alpha, "alpha"),
                horizontalalignment=get_param_value(
                    horizontalalignment, "horizontalalignment"
                ),
                verticalalignment=get_param_value(
                    verticalalignment, "verticalalignment"
                ),
                transform=ax.transData,
                bbox=bbox,
                zorder=1,
                clip_on=clip_on,
                label_pos=get_param_value(label_pos, "label_pos"),
                labels_horizontal=not get_param_value(rotate, "rotate"),
                ax=ax,
            )

    if hide_ticks:
        ax.tick_params(
            axis="both",
            which="both",
            bottom=False,
            left=False,
            labelbottom=False,
            labelleft=False,
        )

    return text_items

