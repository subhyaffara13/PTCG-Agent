
def is_path(f: Any) -> TypeGuard[StrOrBytesPath]:
    return isinstance(f, (bytes, str, os.PathLike))


def is_path(G, path):
    """Returns whether or not the specified path exists.

    For it to return True, every node on the path must exist and
    each consecutive pair must be connected via one or more edges.

    Parameters
    ----------
    G : graph
        A NetworkX graph.

    path : list
        A list of nodes which defines the path to traverse

    Returns
    -------
    bool
        True if `path` is a valid path in `G`

    """
    try:
        return all(nbr in G._adj[node] for node, nbr in nx.utils.pairwise(path))
    except (KeyError, TypeError):
        return False


def is_path(G, path):
    return all(v in G[u] for u, v in pairwise(path))

