
def minimum_spanning_arborescence(
    G, attr="weight", default=1, preserve_attrs=False, partition=None
):
    B = minimal_branching(
        G,
        attr=attr,
        default=default,
        preserve_attrs=preserve_attrs,
        partition=partition,
    )

    if not is_arborescence(B):
        raise nx.exception.NetworkXException("No minimum spanning arborescence in G.")

    return B

