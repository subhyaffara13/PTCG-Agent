import itertools

def makepairs(x, y):
    """Helper function to create an array of pairs of x and y."""
    xy = np.array(list(itertools.product(np.asarray(x), np.asarray(y))))
    return xy.T

