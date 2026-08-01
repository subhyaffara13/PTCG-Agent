
def display(segments: Iterable[Segment], text: str) -> None:
    """Render segments to Jupyter."""
    html = _render_segments(segments)
    jupyter_renderable = JupyterRenderable(html, text)
    try:
        from IPython.display import display as ipython_display

        ipython_display(jupyter_renderable)
    except ModuleNotFoundError:
        # Handle the case where the Console has force_jupyter=True,
        # but IPython is not installed.
        pass


def display(
    value: Any,
    ignore_exceptions: bool = False,
    roundtrip_mode: bool = False,
    autovisualize: bool | autovisualize_lib.Autovisualizer | None = None,
    streaming: bool = True,
    compress_html: bool = True,
):
  """Displays a value as an interactively foldable object.

  Uses the default renderer.

  Args:
    value: Value to display.
    ignore_exceptions: Whether to catch errors during rendering of subtrees and
      show a fallback for those subtrees.
    roundtrip_mode: Whether to start in roundtrip mode.
    autovisualize: Optional autovisualizer override. If True, renders using the
      default autovisualizer (usually an array autovisualizer). If False,
      disables automatic visualization. If a function or object, uses that
      autovisualizer. If None (the default), uses the current active
      autovisualizer (if any) without overriding it.
    streaming: Whether to render in streaming mode, which immediately displays
      the structure of the output while computing more expensive leaf
      renderings. This is useful in interactive contexts, but can mess with
      other users of IPython's formatting because the final rendered HTML is
      empty.
    compress_html: Whether to zlib-compress (i.e. zip) treescope renderings to
      reduce their size when transmitted to the browser or saved into a
      notebook.

  Raises:
    RuntimeError: If IPython is not available.
  """
  if IPython is None:
    raise RuntimeError("Cannot use `display` outside of IPython.")
  with contextlib.ExitStack() as stack:
    if autovisualize is not None:
      if autovisualize is True:  # pylint: disable=g-bool-id-comparison
        tmp_autovisualizer = default_magic_autovisualizer.get()
      elif autovisualize is False:  # pylint: disable=g-bool-id-comparison
        tmp_autovisualizer = None
      else:
        tmp_autovisualizer = autovisualize
      stack.enter_context(
          autovisualize_lib.active_autovisualizer.set_scoped(tmp_autovisualizer)
      )
    maybe_stolen = _display_and_maybe_steal(
        value=value,
        ignore_exceptions=ignore_exceptions,
        roundtrip_mode=roundtrip_mode,
        streaming=streaming,
        compress_html=compress_html,
        stealable=False,
    )
    # Should not get an output when `stealable=False`
    assert maybe_stolen is None


def display(segments: Iterable[Segment], text: str) -> None:
    """Render segments to Jupyter."""
    html = _render_segments(segments)
    jupyter_renderable = JupyterRenderable(html, text)
    try:
        from IPython.display import display as ipython_display

        ipython_display(jupyter_renderable)
    except ModuleNotFoundError:
        # Handle the case where the Console has force_jupyter=True,
        # but IPython is not installed.
        pass


def display(
    G,
    canvas=None,
    **kwargs,
):
    """Draw the graph G.

    Draw the graph as a collection of nodes connected by edges.
    The exact details of what the graph looks like are controlled by the below
    attributes. All nodes and nodes at the end of visible edges must have a
    position set, but nearly all other node and edge attributes are options and
    nodes or edges missing the attribute will use the default listed below. A more
    complete description of each parameter is given below this summary.

    .. list-table:: Default Visualization Attributes
        :widths: 25 25 50
        :header-rows: 1

        * - Parameter
          - Default Attribute
          - Default Value
        * - node_pos
          - `"pos"`
          - If there is not position, a layout will be calculated with `nx.spring_layout`.
        * - node_visible
          - `"visible"`
          - True
        * - node_color
          - `"color"`
          - #1f78b4
        * - node_size
          - `"size"`
          - 300
        * - node_label
          - `"label"`
          - Dict describing the node label. Defaults create a black text with
            the node name as the label. The dict respects these keys and defaults:

            * size : 12
            * color : black
            * family : sans serif
            * weight : normal
            * alpha : 1.0
            * h_align : center
            * v_align : center
            * bbox : Dict describing a `matplotlib.patches.FancyBboxPatch`.
              Default is None.

        * - node_shape
          - `"shape"`
          - "o"
        * - node_alpha
          - `"alpha"`
          - 1.0
        * - node_border_width
          - `"border_width"`
          - 1.0
        * - node_border_color
          - `"border_color"`
          - Matching node_color
        * - edge_visible
          - `"visible"`
          - True
        * - edge_width
          - `"width"`
          - 1.0
        * - edge_color
          - `"color"`
          - Black (#000000)
        * - edge_label
          - `"label"`
          - Dict describing the edge label. Defaults create black text with a
            white bounding box. The dictionary respects these keys and defaults:

            * size : 12
            * color : black
            * family : sans serif
            * weight : normal
            * alpha : 1.0
            * bbox : Dict describing a `matplotlib.patches.FancyBboxPatch`.
              Default {"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0)}
            * h_align : "center"
            * v_align : "center"
            * pos : 0.5
            * rotate : True

        * - edge_style
          - `"style"`
          - "-"
        * - edge_alpha
          - `"alpha"`
          - 1.0
        * - edge_arrowstyle
          - `"arrowstyle"`
          - ``"-|>"`` if `G` is directed else ``"-"``
        * - edge_arrowsize
          - `"arrowsize"`
          - 10 if `G` is directed else 0
        * - edge_curvature
          - `"curvature"`
          - arc3
        * - edge_source_margin
          - `"source_margin"`
          - 0
        * - edge_target_margin
          - `"target_margin"`
          - 0

    Parameters
    ----------
    G : graph
        A networkx graph

    canvas : Matplotlib Axes object, optional
        Draw the graph in specified Matplotlib axes

    node_pos : string or function, default "pos"
        A string naming the node attribute storing the position of nodes as a tuple.
        Or a function to be called with input `G` which returns the layout as a dict keyed
        by node to position tuple like the NetworkX layout functions.
        If no nodes in the graph has the attribute, a spring layout is calculated.

    node_visible : string or bool, default visible
        A string naming the node attribute which stores if a node should be drawn.
        If `True`, all nodes will be visible while if `False` no nodes will be visible.
        If incomplete, nodes missing this attribute will be shown by default.

    node_color : string, default "color"
        A string naming the node attribute which stores the color of each node.
        Visible nodes without this attribute will use '#1f78b4' as a default.

    node_size : string or number, default "size"
        A string naming the node attribute which stores the size of each node.
        Visible nodes without this attribute will use a default size of 300.

    node_label : string or bool, default "label"
        A string naming the node attribute which stores the label of each node.
        The attribute value can be a string, False (no label for that node),
        True (the node is the label) or a dict keyed by node to the label.

        If a dict is specified, these keys are read to further control the label:

        * label : The text of the label; default: name of the node
        * size : Font size of the label; default: 12
        * color : Font color of the label; default: black
        * family : Font family of the label; default: "sans-serif"
        * weight : Font weight of the label; default: "normal"
        * alpha : Alpha value of the label; default: 1.0
        * h_align : The horizontal alignment of the label.
            one of "left", "center", "right"; default: "center"
        * v_align : The vertical alignment of the label.
            one of "top", "center", "bottom"; default: "center"
        * bbox : A dict of parameters for `matplotlib.patches.FancyBboxPatch`.

        Visible nodes without this attribute will be treated as if the value was True.

    node_shape : string, default "shape"
        A string naming the node attribute which stores the label of each node.
        The values of this attribute are expected to be one of the matplotlib shapes,
        one of 'so^>v<dph8'. Visible nodes without this attribute will use 'o'.

    node_alpha : string, default "alpha"
        A string naming the node attribute which stores the alpha of each node.
        The values of this attribute are expected to be floats between 0.0 and 1.0.
        Visible nodes without this attribute will be treated as if the value was 1.0.

    node_border_width : string, default "border_width"
        A string naming the node attribute storing the width of the border of the node.
        The values of this attribute are expected to be numeric. Visible nodes without
        this attribute will use the assumed default of 1.0.

    node_border_color : string, default "border_color"
        A string naming the node attribute which storing the color of the border of the node.
        Visible nodes missing this attribute will use the final node_color value.

    edge_visible : string or bool, default "visible"
        A string nameing the edge attribute which stores if an edge should be drawn.
        If `True`, all edges will be drawn while if `False` no edges will be visible.
        If incomplete, edges missing this attribute will be shown by default. Values
        of this attribute are expected to be booleans.

    edge_width : string or int, default "width"
        A string nameing the edge attribute which stores the width of each edge.
        Visible edges without this attribute will use a default width of 1.0.

    edge_color : string or color, default "color"
        A string nameing the edge attribute which stores of color of each edge.
        Visible edges without this attribute will be drawn black. Each color can be
        a string or rgb (or rgba) tuple of floats from 0.0 to 1.0.

    edge_label : string, default "label"
        A string naming the edge attribute which stores the label of each edge.
        The values of this attribute can be a string, number or False or None. In
        the latter two cases, no edge label is displayed.

        If a dict is specified, these keys are read to further control the label:

        * label : The text of the label, or the name of an edge attribute holding the label.
        * size : Font size of the label; default: 12
        * color : Font color of the label; default: black
        * family : Font family of the label; default: "sans-serif"
        * weight : Font weight of the label; default: "normal"
        * alpha : Alpha value of the label; default: 1.0
        * h_align : The horizontal alignment of the label.
            one of "left", "center", "right"; default: "center"
        * v_align : The vertical alignment of the label.
            one of "top", "center", "bottom"; default: "center"
        * bbox : A dict of parameters for `matplotlib.patches.FancyBboxPatch`.
        * rotate : Whether to rotate labels to lie parallel to the edge, default: True.
        * pos : A float showing how far along the edge to put the label; default: 0.5.

    edge_style : string, default "style"
        A string naming the edge attribute which stores the style of each edge.
        Visible edges without this attribute will be drawn solid. Values of this
        attribute can be line styles, e.g. '-', '--', '-.' or ':' or words like 'solid'
        or 'dashed'. If no edge in the graph has this attribute and it is a non-default
        value, assume that it describes the edge style for all edges in the graph.

    edge_alpha : string or float, default "alpha"
        A string naming the edge attribute which stores the alpha value of each edge.
        Visible edges without this attribute will use an alpha value of 1.0.

    edge_arrowstyle : string, default "arrowstyle"
        A string naming the edge attribute which stores the type of arrowhead to use for
        each edge. Visible edges without this attribute use ``"-"`` for undirected graphs
        and ``"-|>"`` for directed graphs.

        See `matplotlib.patches.ArrowStyle` for more options

    edge_arrowsize : string or int, default "arrowsize"
        A string naming the edge attribute which stores the size of the arrowhead for each
        edge. Visible edges without this attribute will use a default value of 10.

    edge_curvature : string, default "curvature"
       A string naming the edge attribute storing the curvature and connection style
       of each edge. Visible edges without this attribute will use "arc3" as a default
       value, resulting an a straight line between the two nodes. Curvature can be given
       as 'arc3,rad=0.2' to specify both the style and radius of curvature.

       Please see `matplotlib.patches.ConnectionStyle` and
       `matplotlib.patches.FancyArrowPatch` for more information.

    edge_source_margin : string or int, default "source_margin"
        A string naming the edge attribute which stores the minimum margin (gap) between
        the source node and the start of the edge. Visible edges without this attribute
        will use a default value of 0.

    edge_target_margin : string or int, default "target_margin"
        A string naming the edge attribute which stores the minimumm margin (gap) between
        the target node and the end of the edge. Visible edges without this attribute
        will use a default value of 0.

    hide_ticks : bool, default True
        Weather to remove the ticks from the axes of the matplotlib object.

    Raises
    ------
    NetworkXError
        If a node or edge is missing a required parameter such as `pos` or
        if `display` receives an argument not listed above.

    ValueError
        If a node or edge has an invalid color format, i.e. not a color string,
        rgb tuple or rgba tuple.

    Returns
    -------
    The input graph. This is potentially useful for dispatching visualization
    functions.
    """
    from collections import Counter

    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np

    defaults = {
        "node_pos": None,
        "node_visible": True,
        "node_color": "#1f78b4",
        "node_size": 300,
        "node_label": {
            "size": 12,
            "color": "#000000",
            "family": "sans-serif",
            "weight": "normal",
            "alpha": 1.0,
            "h_align": "center",
            "v_align": "center",
            "bbox": None,
        },
        "node_shape": "o",
        "node_alpha": 1.0,
        "node_border_width": 1.0,
        "node_border_color": "face",
        "edge_visible": True,
        "edge_width": 1.0,
        "edge_color": "#000000",
        "edge_label": {
            "size": 12,
            "color": "#000000",
            "family": "sans-serif",
            "weight": "normal",
            "alpha": 1.0,
            "bbox": {"boxstyle": "round", "ec": (1.0, 1.0, 1.0), "fc": (1.0, 1.0, 1.0)},
            "h_align": "center",
            "v_align": "center",
            "pos": 0.5,
            "rotate": True,
        },
        "edge_style": "-",
        "edge_alpha": 1.0,
        "edge_arrowstyle": "-|>" if G.is_directed() else "-",
        "edge_arrowsize": 10 if G.is_directed() else 0,
        "edge_curvature": "arc3",
        "edge_source_margin": 0,
        "edge_target_margin": 0,
        "hide_ticks": True,
    }

    # Check arguments
    for kwarg in kwargs:
        if kwarg not in defaults:
            raise nx.NetworkXError(
                f"Unrecognized visualization keyword argument: {kwarg}"
            )

    if canvas is None:
        canvas = plt.gca()

    if kwargs.get("hide_ticks", defaults["hide_ticks"]):
        canvas.tick_params(
            axis="both",
            which="both",
            bottom=False,
            left=False,
            labelbottom=False,
            labelleft=False,
        )

    ### Helper methods and classes

    def node_property_sequence(seq, attr):
        """Return a list of attribute values for `seq`, using a default if needed"""

        # All node attribute parameters start with "node_"
        param_name = f"node_{attr}"
        default = defaults[param_name]
        attr = kwargs.get(param_name, attr)

        if default is None:
            # raise instead of using non-existant default value
            for n in seq:
                if attr not in node_subgraph.nodes[n]:
                    raise nx.NetworkXError(f"Attribute '{attr}' missing for node {n}")

        # If `attr` is not a graph attr and was explicitly passed as an argument
        # it must be a user-default value. Allow attr=None to tell draw to skip
        # attributes which are on the graph
        if (
            attr is not None
            and nx.get_node_attributes(node_subgraph, attr) == {}
            and any(attr == v for k, v in kwargs.items() if "node" in k)
        ):
            return [attr for _ in seq]

        return [node_subgraph.nodes[n].get(attr, default) for n in seq]

    def compute_colors(color, alpha):
        if isinstance(color, str):
            rgba = mpl.colors.colorConverter.to_rgba(color)
            # Using a non-default alpha value overrides any alpha value in the color
            if alpha != defaults["node_alpha"]:
                return (rgba[0], rgba[1], rgba[2], alpha)
            return rgba

        if isinstance(color, tuple) and len(color) == 3:
            return (color[0], color[1], color[2], alpha)

        if isinstance(color, tuple) and len(color) == 4:
            return color

        raise ValueError(f"Invalid format for color: {color}")

    # Find which edges can be plotted as a line collection
    #
    # Non-default values for these attributes require fancy arrow patches:
    # - any arrow style (including the default -|> for directed graphs)
    # - arrow size (by extension of style)
    # - connection style
    # - min_source_margin
    # - min_target_margin

    def collection_compatible(e):
        return (
            get_edge_attr(e, "arrowstyle") == "-"
            and get_edge_attr(e, "curvature") == "arc3"
            and get_edge_attr(e, "source_margin") == 0
            and get_edge_attr(e, "target_margin") == 0
            # Self-loops will use fancy arrow patches
            and e[0] != e[1]
        )

    def edge_property_sequence(seq, attr):
        """Return a list of attribute values for `seq`, using a default if needed"""

        param_name = f"edge_{attr}"
        default = defaults[param_name]
        attr = kwargs.get(param_name, attr)

        if default is None:
            # raise instead of using non-existant default value
            for e in seq:
                if attr not in edge_subgraph.edges[e]:
                    raise nx.NetworkXError(f"Attribute '{attr}' missing for edge {e}")

        if (
            attr is not None
            and nx.get_edge_attributes(edge_subgraph, attr) == {}
            and any(attr == v for k, v in kwargs.items() if "edge" in k)
        ):
            return [attr for _ in seq]

        return [edge_subgraph.edges[e].get(attr, default) for e in seq]

    def get_edge_attr(e, attr):
        """Return the final edge attribute value, using default if not None"""

        param_name = f"edge_{attr}"
        default = defaults[param_name]
        attr = kwargs.get(param_name, attr)

        if default is None and attr not in edge_subgraph.edges[e]:
            raise nx.NetworkXError(f"Attribute '{attr}' missing from edge {e}")

        if (
            attr is not None
            and nx.get_edge_attributes(edge_subgraph, attr) == {}
            and attr in kwargs.values()
        ):
            return attr

        return edge_subgraph.edges[e].get(attr, default)

    def get_node_attr(n, attr, use_edge_subgraph=True):
        """Return the final node attribute value, using default if not None"""
        subgraph = edge_subgraph if use_edge_subgraph else node_subgraph

        param_name = f"node_{attr}"
        default = defaults[param_name]
        attr = kwargs.get(param_name, attr)

        if default is None and attr not in subgraph.nodes[n]:
            raise nx.NetworkXError(f"Attribute '{attr}' missing from node {n}")

        if (
            attr is not None
            and nx.get_node_attributes(subgraph, attr) == {}
            and attr in kwargs.values()
        ):
            return attr

        return subgraph.nodes[n].get(attr, default)

    # Taken from ConnectionStyleFactory
    def self_loop(edge_index, node_size):
        def self_loop_connection(posA, posB, *args, **kwargs):
            if not np.all(posA == posB):
                raise nx.NetworkXError(
                    "`self_loop` connection style method"
                    "is only to be used for self-loops"
                )
            # this is called with _screen space_ values
            # so convert back to data space
            data_loc = canvas.transData.inverted().transform(posA)
            # Scale self loop based on the size of the base node
            # Size of nodes are given in points ** 2 and each point is 1/72 of an inch
            v_shift = np.sqrt(node_size) / 72
            h_shift = v_shift * 0.5
            # put the top of the loop first so arrow is not hidden by node
            path = np.asarray(
                [
                    # 1
                    [0, v_shift],
                    # 4 4 4
                    [h_shift, v_shift],
                    [h_shift, 0],
                    [0, 0],
                    # 4 4 4
                    [-h_shift, 0],
                    [-h_shift, v_shift],
                    [0, v_shift],
                ]
            )
            # Rotate self loop 90 deg. if more than 1
            # This will allow for maximum of 4 visible self loops
            if edge_index % 4:
                x, y = path.T
                for _ in range(edge_index % 4):
                    x, y = y, -x
                path = np.array([x, y]).T
            return mpl.path.Path(
                canvas.transData.transform(data_loc + path), [1, 4, 4, 4, 4, 4, 4]
            )

        return self_loop_connection

    def to_marker_edge(size, marker):
        if marker in "s^>v<d":
            return np.sqrt(2 * size) / 2
        else:
            return np.sqrt(size) / 2

    def build_fancy_arrow(e):
        source_margin = to_marker_edge(
            get_node_attr(e[0], "size"),
            get_node_attr(e[0], "shape"),
        )
        source_margin = max(
            source_margin,
            get_edge_attr(e, "source_margin"),
        )

        target_margin = to_marker_edge(
            get_node_attr(e[1], "size"),
            get_node_attr(e[1], "shape"),
        )
        target_margin = max(
            target_margin,
            get_edge_attr(e, "target_margin"),
        )
        return mpl.patches.FancyArrowPatch(
            edge_subgraph.nodes[e[0]][pos],
            edge_subgraph.nodes[e[1]][pos],
            arrowstyle=get_edge_attr(e, "arrowstyle"),
            connectionstyle=(
                get_edge_attr(e, "curvature")
                if e[0] != e[1]
                else self_loop(
                    0 if len(e) == 2 else e[2] % 4,
                    get_node_attr(e[0], "size"),
                )
            ),
            color=get_edge_attr(e, "color"),
            linestyle=get_edge_attr(e, "style"),
            linewidth=get_edge_attr(e, "width"),
            mutation_scale=get_edge_attr(e, "arrowsize"),
            shrinkA=source_margin,
            shrinkB=source_margin,
            zorder=1,
        )

    class CurvedArrowText(CurvedArrowTextBase, mpl.text.Text):
        pass

    ### Draw the nodes first
    node_visible = kwargs.get("node_visible", "visible")
    if isinstance(node_visible, bool):
        if node_visible:
            visible_nodes = G.nodes()
        else:
            visible_nodes = []
    else:
        visible_nodes = [
            n for n, v in nx.get_node_attributes(G, node_visible, True).items() if v
        ]

    node_subgraph = G.subgraph(visible_nodes)

    # Ignore the default dict value since that's for default values to use, not
    # default attribute name
    pos = kwargs.get("node_pos", "pos")

    default_display_pos_attr = "display's position attribute name"
    if callable(pos):
        nx.set_node_attributes(
            node_subgraph, pos(node_subgraph), default_display_pos_attr
        )
        pos = default_display_pos_attr
        kwargs["node_pos"] = default_display_pos_attr
    elif nx.get_node_attributes(G, pos) == {}:
        nx.set_node_attributes(
            node_subgraph, nx.spring_layout(node_subgraph), default_display_pos_attr
        )
        pos = default_display_pos_attr
        kwargs["node_pos"] = default_display_pos_attr

    # Each shape requires a new scatter object since they can't have different
    # shapes.
    if len(visible_nodes) > 0:
        node_shape = kwargs.get("node_shape", "shape")
        for shape in Counter(
            nx.get_node_attributes(
                node_subgraph, node_shape, defaults["node_shape"]
            ).values()
        ):
            # Filter position just on this shape.
            nodes_with_shape = [
                n
                for n, s in node_subgraph.nodes(data=node_shape)
                if s == shape or (s is None and shape == defaults["node_shape"])
            ]
            # There are two property sequences to create before hand.
            # 1. position, since it is used for x and y parameters to scatter
            # 2. edgecolor, since the spaeical 'face' parameter value can only be
            #    be passed in as the sole string, not part of a list of strings.
            position = np.asarray(node_property_sequence(nodes_with_shape, "pos"))
            color = np.asarray(
                [
                    compute_colors(c, a)
                    for c, a in zip(
                        node_property_sequence(nodes_with_shape, "color"),
                        node_property_sequence(nodes_with_shape, "alpha"),
                    )
                ]
            )
            border_color = np.asarray(
                [
                    (
                        c
                        if (
                            c := get_node_attr(
                                n,
                                "border_color",
                                False,
                            )
                        )
                        != "face"
                        else color[i]
                    )
                    for i, n in enumerate(nodes_with_shape)
                ]
            )
            canvas.scatter(
                position[:, 0],
                position[:, 1],
                s=node_property_sequence(nodes_with_shape, "size"),
                c=color,
                marker=shape,
                linewidths=node_property_sequence(nodes_with_shape, "border_width"),
                edgecolors=border_color,
                zorder=2,
            )

    ### Draw node labels
    node_label = kwargs.get("node_label", "label")
    # Plot labels if node_label is not None and not False
    if node_label is not None and node_label is not False:
        default_dict = {}
        if isinstance(node_label, dict):
            default_dict = node_label
            node_label = None

        for n, lbl in node_subgraph.nodes(data=node_label):
            if lbl is False:
                continue

            # We work with label dicts down here...
            if not isinstance(lbl, dict):
                lbl = {"label": lbl if lbl is not None else n}

            lbl_text = lbl.get("label", n)
            if not isinstance(lbl_text, str):
                lbl_text = str(lbl_text)

            lbl.update(default_dict)
            x, y = node_subgraph.nodes[n][pos]
            canvas.text(
                x,
                y,
                lbl_text,
                size=lbl.get("size", defaults["node_label"]["size"]),
                color=lbl.get("color", defaults["node_label"]["color"]),
                family=lbl.get("family", defaults["node_label"]["family"]),
                weight=lbl.get("weight", defaults["node_label"]["weight"]),
                horizontalalignment=lbl.get(
                    "h_align", defaults["node_label"]["h_align"]
                ),
                verticalalignment=lbl.get("v_align", defaults["node_label"]["v_align"]),
                transform=canvas.transData,
                bbox=lbl.get("bbox", defaults["node_label"]["bbox"]),
            )

    ### Draw edges

    edge_visible = kwargs.get("edge_visible", "visible")
    if isinstance(edge_visible, bool):
        if edge_visible:
            visible_edges = G.edges()
        else:
            visible_edges = []
    else:
        visible_edges = [
            e for e, v in nx.get_edge_attributes(G, edge_visible, True).items() if v
        ]

    edge_subgraph = G.edge_subgraph(visible_edges)
    nx.set_node_attributes(
        edge_subgraph, nx.get_node_attributes(node_subgraph, pos), name=pos
    )

    collection_edges = (
        [e for e in edge_subgraph.edges(keys=True) if collection_compatible(e)]
        if edge_subgraph.is_multigraph()
        else [e for e in edge_subgraph.edges() if collection_compatible(e)]
    )
    non_collection_edges = (
        [e for e in edge_subgraph.edges(keys=True) if not collection_compatible(e)]
        if edge_subgraph.is_multigraph()
        else [e for e in edge_subgraph.edges() if not collection_compatible(e)]
    )
    edge_position = np.asarray(
        [
            (
                get_node_attr(u, "pos", use_edge_subgraph=True),
                get_node_attr(v, "pos", use_edge_subgraph=True),
            )
            for u, v, *_ in collection_edges
        ]
    )

    # Only plot a line collection if needed
    if len(collection_edges) > 0:
        edge_collection = mpl.collections.LineCollection(
            edge_position,
            colors=edge_property_sequence(collection_edges, "color"),
            linewidths=edge_property_sequence(collection_edges, "width"),
            linestyle=edge_property_sequence(collection_edges, "style"),
            alpha=edge_property_sequence(collection_edges, "alpha"),
            antialiaseds=(1,),
            zorder=1,
        )
        canvas.add_collection(edge_collection)

    fancy_arrows = {}
    if len(non_collection_edges) > 0:
        for e in non_collection_edges:
            # Cache results for use in edge labels
            fancy_arrows[e] = build_fancy_arrow(e)
            canvas.add_patch(fancy_arrows[e])

    ### Draw edge labels
    edge_label = kwargs.get("edge_label", "label")
    default_dict = {}
    if isinstance(edge_label, dict):
        default_dict = edge_label
        # Restore the default label attribute key of 'label'
        edge_label = "label"

    # Handle multigraphs
    edge_label_data = (
        edge_subgraph.edges(data=edge_label, keys=True)
        if edge_subgraph.is_multigraph()
        else edge_subgraph.edges(data=edge_label)
    )
    if edge_label is not None and edge_label is not False:
        for *e, lbl in edge_label_data:
            e = tuple(e)
            # I'm not sure how I want to handle None here... For now it means no label
            if lbl is False or lbl is None:
                continue

            if not isinstance(lbl, dict):
                lbl = {"label": lbl}

            lbl.update(default_dict)
            lbl_text = lbl.get("label")
            if not isinstance(lbl_text, str):
                lbl_text = str(lbl_text)

            # In the old code, every non-self-loop is placed via a fancy arrow patch
            # Only compute a new fancy arrow if needed by caching the results from
            # edge placement.
            try:
                arrow = fancy_arrows[e]
            except KeyError:
                arrow = build_fancy_arrow(e)

            if e[0] == e[1]:
                # Taken directly from draw_networkx_edge_labels
                connectionstyle_obj = arrow.get_connectionstyle()
                posA = canvas.transData.transform(edge_subgraph.nodes[e[0]][pos])
                path_disp = connectionstyle_obj(posA, posA)
                path_data = canvas.transData.inverted().transform_path(path_disp)
                x, y = path_data.vertices[0]
                canvas.text(
                    x,
                    y,
                    lbl_text,
                    size=lbl.get("size", defaults["edge_label"]["size"]),
                    color=lbl.get("color", defaults["edge_label"]["color"]),
                    family=lbl.get("family", defaults["edge_label"]["family"]),
                    weight=lbl.get("weight", defaults["edge_label"]["weight"]),
                    alpha=lbl.get("alpha", defaults["edge_label"]["alpha"]),
                    horizontalalignment=lbl.get(
                        "h_align", defaults["edge_label"]["h_align"]
                    ),
                    verticalalignment=lbl.get(
                        "v_align", defaults["edge_label"]["v_align"]
                    ),
                    rotation=0,
                    transform=canvas.transData,
                    bbox=lbl.get("bbox", defaults["edge_label"]["bbox"]),
                    zorder=1,
                )
                continue

            CurvedArrowText(
                arrow,
                lbl_text,
                size=lbl.get("size", defaults["edge_label"]["size"]),
                color=lbl.get("color", defaults["edge_label"]["color"]),
                family=lbl.get("family", defaults["edge_label"]["family"]),
                weight=lbl.get("weight", defaults["edge_label"]["weight"]),
                alpha=lbl.get("alpha", defaults["edge_label"]["alpha"]),
                bbox=lbl.get("bbox", defaults["edge_label"]["bbox"]),
                horizontalalignment=lbl.get(
                    "h_align", defaults["edge_label"]["h_align"]
                ),
                verticalalignment=lbl.get("v_align", defaults["edge_label"]["v_align"]),
                label_pos=lbl.get("pos", defaults["edge_label"]["pos"]),
                labels_horizontal=lbl.get("rotate", defaults["edge_label"]["rotate"]),
                transform=canvas.transData,
                zorder=1,
                ax=canvas,
            )

    # If we had to add an attribute, remove it here
    if pos == default_display_pos_attr:
        nx.remove_node_attributes(G, default_display_pos_attr)

    return G


def display(*args):
  """Display the given objects using the Treescope pretty-printer.

  If treescope is not installed or the code is not running in IPython,
  ``display`` will print the objects instead.
  """
  if not in_ipython:
    for x in args:
      print(x)
    return

  for x in args:
    treescope.display(x, ignore_exceptions=True, autovisualize=True)

