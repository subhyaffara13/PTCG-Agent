from typing import Any

def visualize_min_cut_graph(
    nx_graph: nx.DiGraph[str, dict[str, Any]],
) -> tuple[str | None, str | None]:
    """Visualize the min-cut graph to an SVG file.

    Returns (path_to_svg, svg_content) tuple. Both are None if pydot is unavailable.
    """
    import networkx as nx

    try:
        import pydot
    except ImportError:
        log.info(
            "Install pydot to visualize the min-cut graph for debugging: pip install pydot",
            exc_info=True,
        )
        return None, None

    dot_format = nx.nx_pydot.to_pydot(nx_graph).to_string()
    dot_graph = pydot.graph_from_dot_data(dot_format)[0]  # type: ignore[index]
    for edge in dot_graph.get_edges():
        weight = nx_graph[edge.get_source()][edge.get_destination()]["capacity"]
        # Set edge label to weight
        edge.set_label(str(weight))  # type: ignore[union-attr]
        # Color edges with weight 'inf' as red
        if weight == float("inf"):
            edge.set_color("red")  # type: ignore[union-attr]

    # Generate SVG content
    svg_content = dot_graph.create_svg().decode("utf-8")  # type: ignore[union-attr]

    # Write to local file
    svg_path = _get_unique_path("min_cut_failed", ".svg")
    with open(svg_path, "w") as f:
        f.write(svg_content)

    return svg_path, svg_content

