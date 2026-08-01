
def _untabulate(table):
    # converts a contingency table to paired samples indicating the
    # correspondence between row and column indices
    r, c = table.shape
    x, y = [], []
    for i in range(r):
        for j in range(c):
            x.append([i] * table[i, j])
            y.append([j] * table[i, j])
    return np.concatenate(x), np.concatenate(y)

