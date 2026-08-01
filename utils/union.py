
def union(*args, **kwargs):
    return UnionNode(*args, **kwargs)


def union(G, H, rename=()):
    """Combine graphs G and H. The names of nodes must be unique.

    A name collision between the graphs will raise an exception.

    A renaming facility is provided to avoid name collisions.


    Parameters
    ----------
    G, H : graph
       A NetworkX graph

    rename : iterable , optional
       Node names of G and H can be changed by specifying the tuple
       rename=('G-','H-') (for example).  Node "u" in G is then renamed
       "G-u" and "v" in H is renamed "H-v".

    Returns
    -------
    U : A union graph with the same type as G.

    See Also
    --------
    compose
    :func:`~networkx.Graph.update`
    disjoint_union

    Notes
    -----
    To combine graphs that have common nodes, consider compose(G, H)
    or the method, Graph.update().

    disjoint_union() is similar to union() except that it avoids name clashes
    by relabeling the nodes with sequential integers.

    Edge and node attributes are propagated from G and H to the union graph.
    Graph attributes are also propagated, but if they are present in both G and H,
    then the value from H is used.

    Examples
    --------
    >>> from pprint import pprint
    >>> G = nx.Graph([(0, 1), (0, 2), (1, 2)])
    >>> H = nx.Graph([(0, 1), (0, 3), (1, 3), (1, 2)])
    >>> U = nx.union(G, H, rename=("G", "H"))
    >>> U.nodes
    NodeView(('G0', 'G1', 'G2', 'H0', 'H1', 'H3', 'H2'))
    >>> edgelist = list(U.edges)
    >>> pprint(edgelist)
    [('G0', 'G1'),
     ('G0', 'G2'),
     ('G1', 'G2'),
     ('H0', 'H1'),
     ('H0', 'H3'),
     ('H1', 'H3'),
     ('H1', 'H2')]


    """
    return nx.union_all([G, H], rename)

