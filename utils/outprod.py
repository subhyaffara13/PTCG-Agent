
def outprod(x, y):
    if not USE_NAIVE_MATH:
        return np.outer(x, y)
    result = np.zeros((len(x), len(y)))
    for i in range(len(x)):
            result[:, i] = x * y[i]
    return result

