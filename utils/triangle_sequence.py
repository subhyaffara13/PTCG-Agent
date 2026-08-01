
def triangle_sequence(creation_sequence):
    """
    Return triangle sequence for the given threshold graph creation sequence.

    """
    cs = creation_sequence
    seq = []
    dr = cs.count("d")  # number of d's to the right of the current pos
    dcur = (dr - 1) * (dr - 2) // 2  # number of triangles through a node of clique dr
    irun = 0  # number of i's in the last run
    drun = 0  # number of d's in the last run
    for i, sym in enumerate(cs):
        if sym == "d":
            drun += 1
            tri = dcur + (dr - 1) * irun  # new triangles at this d
        else:  # cs[i]="i":
            if prevsym == "d":  # new string of i's
                dcur += (dr - 1) * irun  # accumulate shared shortest paths
                irun = 0  # reset i run counter
                dr -= drun  # reduce number of d's to right
                drun = 0  # reset d run counter
            irun += 1
            tri = dr * (dr - 1) // 2  # new triangles at this i
        seq.append(tri)
        prevsym = sym
    return seq

