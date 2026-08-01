
def matprod22(x, y):
    result = np.zeros((x.shape[0], y.shape[1]))
    for i in range(y.shape[1]):
        for j in range(x.shape[1]):
            result[:, j] += x[:, i] * y[i, j]
    return result

