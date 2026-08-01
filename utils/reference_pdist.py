
def reference_pdist(input, p=2):
    pdist = scipy.spatial.distance.pdist
    if p == 0:
        output = pdist(input, "hamming") * input.shape[1]
    elif p == float("inf"):
        output = pdist(input, lambda x, y: np.abs(x - y).max())
    else:
        output = pdist(input, "minkowski", p=p)
    return output.astype(input.dtype)

