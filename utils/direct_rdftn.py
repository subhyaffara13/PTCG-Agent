
def direct_rdftn(x):
    return fftn(rfft(x), axes=range(x.ndim - 1))

