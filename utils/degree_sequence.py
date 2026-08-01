
def degree_sequence(creation_sequence):
    """
    Return degree sequence for the threshold graph with the given
    creation sequence
    """
    cs = creation_sequence  # alias
    seq = []
    rd = cs.count("d")  # number of d to the right
    for i, sym in enumerate(cs):
        if sym == "d":
            rd -= 1
            seq.append(rd + i)
        else:
            seq.append(rd)
    return seq

