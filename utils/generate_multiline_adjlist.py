
def generate_multiline_adjlist(G, delimiter=" "):
    """Generate a single line of the graph G in multiline adjacency list format.

    Parameters
    ----------
    G : NetworkX graph

    delimiter : string, optional
       Separator for node labels

    Returns
    -------
    lines : string
        Lines of data in multiline adjlist format.

    Examples
    --------
    >>> G = nx.lollipop_graph(4, 3)
    >>> for line in nx.generate_multiline_adjlist(G):
    ...     print(line)
    0 3
    1 {}
    2 {}
    3 {}
    1 2
    2 {}
    3 {}
    2 1
    3 {}
    3 1
    4 {}
    4 1
    5 {}
    5 1
    6 {}
    6 0

    See Also
    --------
    write_multiline_adjlist, read_multiline_adjlist
    """
    if G.is_directed():
        if G.is_multigraph():
            for s, nbrs in G.adjacency():
                nbr_edges = [
                    (u, data)
                    for u, datadict in nbrs.items()
                    for key, data in datadict.items()
                ]
                deg = len(nbr_edges)
                yield str(s) + delimiter + str(deg)
                for u, d in nbr_edges:
                    if d is None:
                        yield str(u)
                    else:
                        yield str(u) + delimiter + str(d)
        else:  # directed single edges
            for s, nbrs in G.adjacency():
                deg = len(nbrs)
                yield str(s) + delimiter + str(deg)
                for u, d in nbrs.items():
                    if d is None:
                        yield str(u)
                    else:
                        yield str(u) + delimiter + str(d)
    else:  # undirected
        if G.is_multigraph():
            seen = set()  # helper dict used to avoid duplicate edges
            for s, nbrs in G.adjacency():
                nbr_edges = [
                    (u, data)
                    for u, datadict in nbrs.items()
                    if u not in seen
                    for key, data in datadict.items()
                ]
                deg = len(nbr_edges)
                yield str(s) + delimiter + str(deg)
                for u, d in nbr_edges:
                    if d is None:
                        yield str(u)
                    else:
                        yield str(u) + delimiter + str(d)
                seen.add(s)
        else:  # undirected single edges
            seen = set()  # helper dict used to avoid duplicate edges
            for s, nbrs in G.adjacency():
                nbr_edges = [(u, d) for u, d in nbrs.items() if u not in seen]
                deg = len(nbr_edges)
                yield str(s) + delimiter + str(deg)
                for u, d in nbr_edges:
                    if d is None:
                        yield str(u)
                    else:
                        yield str(u) + delimiter + str(d)
                seen.add(s)

