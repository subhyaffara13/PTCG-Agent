
def primasum(x, axis=None):
    '''
    According to its documentation, np.sum will sometimes do partial pairwise summation.
    For our purposes, when comparing, we want don't want to do anything fancy, and we
    just want to add things up one at a time.
    '''
    if not USE_NAIVE_MATH:
        return np.sum(x, axis=axis)
    if axis is None:
        if x.ndim == 2:
            # Sum columns first, then sum the result
            return sum(primasum(x, axis=0))
        else:
            return sum(x)
    elif axis == 0:
        result = np.zeros(x.shape[1])
        for i in range(x.shape[1]):
            result[i] = sum(x[:, i])
        return result
    elif axis == 1:
        result = np.zeros(x.shape[0])
        for i in range(x.shape[0]):
            result[i] = sum(x[i, :])
        return result

