
def betweenness_sequence(creation_sequence, normalized=True):
    """
    Return betweenness for the threshold graph with the given creation
    sequence.  The result is unscaled.  To scale the values
    to the interval [0,1] divide by (n-1)*(n-2).
    """
    cs = creation_sequence
    seq = []  # betweenness
    lastchar = "d"  # first node is always a 'd'
    dr = float(cs.count("d"))  # number of d's to the right of current pos
    irun = 0  # number of i's in the last run
    drun = 0  # number of d's in the last run
    dlast = 0.0  # betweenness of last d
    for i, c in enumerate(cs):
        if c == "d":  # cs[i]=="d":
            # betweenness = amt shared with earlier d's and i's
            #             + new isolated nodes covered
            #             + new paths to all previous nodes
            b = dlast + (irun - 1) * irun / dr + 2 * irun * (i - drun - irun) / dr
            drun += 1  # update counter
        else:  # cs[i]="i":
            if lastchar == "d":  # if this is a new run of i's
                dlast = b  # accumulate betweenness
                dr -= drun  # update number of d's to the right
                drun = 0  # reset d counter
                irun = 0  # reset i counter
            b = 0  # isolated nodes have zero betweenness
            irun += 1  # add another i to the run
        seq.append(float(b))
        lastchar = c

    # normalize by the number of possible shortest paths
    if normalized:
        order = len(cs)
        scale = 1.0 / ((order - 1) * (order - 2))
        seq = [s * scale for s in seq]

    return seq

