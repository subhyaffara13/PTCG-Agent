
def is_threshold_sequence(degree_sequence):
    """
    Returns True if the sequence is a threshold degree sequence.

    Uses the property that a threshold graph must be constructed by
    adding either dominating or isolated nodes. Thus, it can be
    deconstructed iteratively by removing a node of degree zero or a
    node that connects to the remaining nodes.  If this deconstruction
    fails then the sequence is not a threshold sequence.
    """
    ds = degree_sequence[:]  # get a copy so we don't destroy original
    ds.sort()
    while ds:
        if ds[0] == 0:  # if isolated node
            ds.pop(0)  # remove it
            continue
        if ds[-1] != len(ds) - 1:  # is the largest degree node dominating?
            return False  # no, not a threshold degree sequence
        ds.pop()  # yes, largest is the dominating node
        ds = [d - 1 for d in ds]  # remove it and decrement all degrees
    return True

