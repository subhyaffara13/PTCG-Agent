
def istril(A, tol=0):
    return primasum(abs(A) - np.tril(abs(A))) <= tol

