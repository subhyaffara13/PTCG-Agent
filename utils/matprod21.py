
def matprod21(x, y):
    result = np.zeros(x.shape[0])
    for i in range(x.shape[1]):
        result += x[:, i] * y[i]
    return result

