
def not_implemented_for(*graph_types):
    """Decorator to mark algorithms as not implemented

    Parameters
    ----------
    graph_types : container of strings
        Entries must be one of "directed", "undirected", "multigraph", or "graph".

    Returns
    -------
    _require : function
        The decorated function.

    Raises
    ------
    NetworkXNotImplemented
    If any of the packages cannot be imported

    Notes
    -----
    Multiple types are joined logically with "and".
    For "or" use multiple @not_implemented_for() lines.

    Examples
    --------
    Decorate functions like this::

       @not_implemented_for("directed")
       def sp_function(G):
           pass


       # rule out MultiDiGraph
       @not_implemented_for("directed", "multigraph")
       def sp_np_function(G):
           pass


       # rule out all except DiGraph
       @not_implemented_for("undirected")
       @not_implemented_for("multigraph")
       def sp_np_function(G):
           pass
    """
    if ("directed" in graph_types) and ("undirected" in graph_types):
        raise ValueError("Function not implemented on directed AND undirected graphs?")
    if ("multigraph" in graph_types) and ("graph" in graph_types):
        raise ValueError("Function not implemented on graph AND multigraphs?")
    if not set(graph_types) < {"directed", "undirected", "multigraph", "graph"}:
        raise KeyError(
            "use one or more of directed, undirected, multigraph, graph.  "
            f"You used {graph_types}"
        )

    # 3-way logic: True if "directed" input, False if "undirected" input, else None
    dval = ("directed" in graph_types) or "undirected" not in graph_types and None
    mval = ("multigraph" in graph_types) or "graph" not in graph_types and None
    errmsg = f"not implemented for {' '.join(graph_types)} type"

    def _not_implemented_for(g):
        if (mval is None or mval == g.is_multigraph()) and (
            dval is None or dval == g.is_directed()
        ):
            raise nx.NetworkXNotImplemented(errmsg)

        return g

    return argmap(_not_implemented_for, 0)

