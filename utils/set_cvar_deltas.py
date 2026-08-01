
def setCvarDeltas(cvt, deltas):
    for i, delta in enumerate(deltas):
        if delta:
            cvt[i] += otRound(delta)

