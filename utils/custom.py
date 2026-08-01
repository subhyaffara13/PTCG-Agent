
def custom(X):
    return scipy.linalg.solve(X, expm(X) - np.eye(X.shape[0]))

