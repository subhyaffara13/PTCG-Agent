
def inprod(x, y):
    if not USE_NAIVE_MATH:
        return np.dot(x, y)
    result = 0
    for i in range(len(x)):
        result += x[i] * y[i]
    return result

