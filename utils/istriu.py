
def istriu(A, tol=0):
    return primasum(abs(A) - np.triu(abs(A))) <= tol

