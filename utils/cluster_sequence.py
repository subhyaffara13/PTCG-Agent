
def cluster_sequence(creation_sequence):
    """
    Return cluster sequence for the given threshold graph creation sequence.
    """
    triseq = triangle_sequence(creation_sequence)
    degseq = degree_sequence(creation_sequence)
    cseq = []
    for i, deg in enumerate(degseq):
        tri = triseq[i]
        if deg <= 1:  # isolated vertex or single pair gets cc 0
            cseq.append(0)
            continue
        max_size = (deg * (deg - 1)) // 2
        cseq.append(tri / max_size)
    return cseq

