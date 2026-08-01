
def _edge_value(G, edge_attr):
    """Returns a function that returns a value from G[u][v].

    Suppose there exists an edge between u and v.  Then we return a function
    expecting u and v as arguments.  For Graph and DiGraph, G[u][v] is
    the edge attribute dictionary, and the function (essentially) returns
    G[u][v][edge_attr].  However, we also handle cases when `edge_attr` is None
    and when it is a function itself. For MultiGraph and MultiDiGraph, G[u][v]
    is a dictionary of all edges between u and v.  In this case, the returned
    function sums the value of `edge_attr` for every edge between u and v.

    Parameters
    ----------
    G : graph
       A NetworkX graph

    edge_attr : {None, str, callable}
        Specification of how the value of the edge attribute should be obtained
        from the edge attribute dictionary, G[u][v].  For multigraphs, G[u][v]
        is a dictionary of all the edges between u and v.  This allows for
        special treatment of multiedges.

    Returns
    -------
    value : function
        A function expecting two nodes as parameters. The nodes should
        represent the from- and to- node of an edge. The function will
        return a value from G[u][v] that depends on `edge_attr`.

    """

    if edge_attr is None:
        # topological count of edges

        if G.is_multigraph():

            def value(u, v):
                return len(G[u][v])

        else:

            def value(u, v):
                return 1

    elif not callable(edge_attr):
        # assume it is a key for the edge attribute dictionary

        if edge_attr == "weight":
            # provide a default value
            if G.is_multigraph():

                def value(u, v):
                    return sum(d.get(edge_attr, 1) for d in G[u][v].values())

            else:

                def value(u, v):
                    return G[u][v].get(edge_attr, 1)

        else:
            # otherwise, the edge attribute MUST exist for each edge
            if G.is_multigraph():

                def value(u, v):
                    return sum(d[edge_attr] for d in G[u][v].values())

            else:

                def value(u, v):
                    return G[u][v][edge_attr]

    else:
        # Advanced:  Allow users to specify something else.
        #
        # Alternative default value:
        #     edge_attr = lambda u,v: G[u][v].get('thickness', .5)
        #
        # Function on an attribute:
        #     edge_attr = lambda u,v: abs(G[u][v]['weight'])
        #
        # Handle Multi(Di)Graphs differently:
        #     edge_attr = lambda u,v: numpy.prod([d['size'] for d in G[u][v].values()])
        #
        # Ignore multiple edges
        #     edge_attr = lambda u,v: 1 if len(G[u][v]) else 0
        #
        value = edge_attr

    return value

