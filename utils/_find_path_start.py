
def _find_path_start(G):
    """Return a suitable starting vertex for an Eulerian path.

    If no path exists, return None.
    """
    if not has_eulerian_path(G):
        return None

    if is_eulerian(G):
        return arbitrary_element(G)

    if G.is_directed():
        v1, v2 = (v for v in G if G.in_degree(v) != G.out_degree(v))
        # Determines which is the 'start' node (as opposed to the 'end')
        if G.out_degree(v1) > G.in_degree(v1):
            return v1
        else:
            return v2

    else:
        # In an undirected graph randomly choose one of the possibilities
        start = [v for v in G if G.degree(v) % 2 != 0][0]
        return start

