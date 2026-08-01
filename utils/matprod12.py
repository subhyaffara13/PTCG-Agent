
def matprod12(x, y):
    result = np.zeros(y.shape[1])
    for i in range(y.shape[1]):
        result[i] = inprod(x, y[:, i])
    return result

