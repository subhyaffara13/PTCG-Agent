
def weights_to_creation_sequence(
    weights, threshold=1, with_labels=False, compact=False
):
    """
    Returns a creation sequence for a threshold graph
    determined by the weights and threshold given as input.
    If the sum of two node weights is greater than the
    threshold value, an edge is created between these nodes.

    The creation sequence is a list of single characters 'd'
    or 'i': 'd' for dominating or 'i' for isolated vertices.
    Dominating vertices are connected to all vertices present
    when it is added.  The first node added is by convention 'd'.

    If with_labels==True:
    Returns a list of 2-tuples containing the vertex number
    and a character 'd' or 'i' which describes the type of vertex.

    If compact==True:
    Returns the creation sequence in a compact form that is the number
    of 'i's and 'd's alternating.
    Examples:
    [1,2,2,3] represents d,i,i,d,d,i,i,i
    [3,1,2] represents d,d,d,i,d,d

    Notice that the first number is the first vertex to be used for
    construction and so is always 'd'.

    with_labels and compact cannot both be True.
    """
    if with_labels and compact:
        raise ValueError("compact sequences cannot be labeled")

    # make an indexed copy
    if isinstance(weights, dict):  # labeled weights
        wseq = [[w, label] for (label, w) in weights.items()]
    else:
        wseq = [[w, i] for i, w in enumerate(weights)]
    wseq.sort()
    cs = []  # creation sequence
    cutoff = threshold - wseq[-1][0]
    while wseq:
        if wseq[0][0] < cutoff:  # isolated node
            (w, label) = wseq.pop(0)
            cs.append((label, "i"))
        else:
            (w, label) = wseq.pop()
            cs.append((label, "d"))
            cutoff = threshold - wseq[-1][0]
        if len(wseq) == 1:  # make sure we start with a d
            (w, label) = wseq.pop()
            cs.append((label, "d"))
    # put in correct order
    cs.reverse()

    if with_labels:
        return cs
    if compact:
        return make_compact(cs)
    return [v[1] for v in cs]  # not labeled

