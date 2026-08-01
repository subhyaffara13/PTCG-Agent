
def read_dot(path):
    """Returns a NetworkX graph from a dot file on path.

    Parameters
    ----------
    path : file or string
       File name or file handle to read.
    """
    try:
        import pygraphviz
    except ImportError as err:
        raise ImportError(
            "read_dot() requires pygraphviz http://pygraphviz.github.io/"
        ) from err
    A = pygraphviz.AGraph(file=path)
    gr = from_agraph(A)
    A.clear()
    return gr


def read_dot(path):
    """Returns a NetworkX :class:`MultiGraph` or :class:`MultiDiGraph` from the
    dot file with the passed path.

    If this file contains multiple graphs, only the first such graph is
    returned. All graphs _except_ the first are silently ignored.

    Parameters
    ----------
    path : str or file
        Filename or file handle to read.
        Filenames ending in .gz or .bz2 will be decompressed.

    Returns
    -------
    G : MultiGraph or MultiDiGraph
        A :class:`MultiGraph` or :class:`MultiDiGraph`.

    Notes
    -----
    Use `G = nx.Graph(nx.nx_pydot.read_dot(path))` to return a :class:`Graph` instead of a
    :class:`MultiGraph`.
    """
    import pydot

    data = path.read()

    # List of one or more "pydot.Dot" instances deserialized from this file.
    P_list = pydot.graph_from_dot_data(data)

    # Convert only the first such instance into a NetworkX graph.
    return from_pydot(P_list[0])

