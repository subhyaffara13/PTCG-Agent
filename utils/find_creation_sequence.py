
def find_creation_sequence(G):
    """
    Find a threshold subgraph that is close to largest in G.
    Returns the labeled creation sequence of that threshold graph.
    """
    cs = []
    # get a local pointer to the working part of the graph
    H = G
    while H.order() > 0:
        # get new degree sequence on subgraph
        dsdict = dict(H.degree())
        ds = [(d, v) for v, d in dsdict.items()]
        ds.sort()
        # Update threshold graph nodes
        if ds[-1][0] == 0:  # all are isolated
            cs.extend(zip(dsdict, ["i"] * (len(ds) - 1) + ["d"]))
            break  # Done!
        # pull off isolated nodes
        while ds[0][0] == 0:
            (d, iso) = ds.pop(0)
            cs.append((iso, "i"))
        # find new biggest node
        (d, bigv) = ds.pop()
        # add edges of star to t_g
        cs.append((bigv, "d"))
        # form subgraph of neighbors of big node
        H = H.subgraph(H.neighbors(bigv))
    cs.reverse()
    return cs

