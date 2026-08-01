
def maximum_spanning_arborescence(
    G, attr="weight", default=1, preserve_attrs=False, partition=None
):
    # In order to use the same algorithm is the maximum branching, we need to adjust
    # the weights of the graph. The branching algorithm can choose to not include an
    # edge if it doesn't help find a branching, mainly triggered by edges with negative
    # weights.
    #
    # To prevent this from happening while trying to find a spanning arborescence, we
    # just have to tweak the edge weights so that they are all positive and cannot
    # become negative during the branching algorithm, find the maximum branching and
    # then return them to their original values.

    min_weight = INF
    max_weight = -INF
    for _, _, w in G.edges(data=attr, default=default):
        if w < min_weight:
            min_weight = w
        if w > max_weight:
            max_weight = w

    for _, _, d in G.edges(data=True):
        d[attr] = d.get(attr, default) - min_weight + 1 - (min_weight - max_weight)
    nx._clear_cache(G)

    B = maximum_branching(G, attr, default, preserve_attrs, partition)

    for _, _, d in G.edges(data=True):
        d[attr] = d.get(attr, default) + min_weight - 1 + (min_weight - max_weight)
    nx._clear_cache(G)

    for _, _, d in B.edges(data=True):
        d[attr] = d.get(attr, default) + min_weight - 1 + (min_weight - max_weight)
    nx._clear_cache(B)

    if not is_arborescence(B):
        raise nx.exception.NetworkXException("No maximum spanning arborescence in G.")

    return B

