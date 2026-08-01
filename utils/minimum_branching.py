
def minimum_branching(
    G, attr="weight", default=1, preserve_attrs=False, partition=None
):
    for _, _, d in G.edges(data=True):
        d[attr] = -d.get(attr, default)
    nx._clear_cache(G)

    B = maximum_branching(G, attr, default, preserve_attrs, partition)

    for _, _, d in G.edges(data=True):
        d[attr] = -d.get(attr, default)
    nx._clear_cache(G)

    for _, _, d in B.edges(data=True):
        d[attr] = -d.get(attr, default)
    nx._clear_cache(B)

    return B

