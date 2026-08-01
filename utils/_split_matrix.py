
def _split_matrix(X, n):
    # definitions according to Seeded Graph Matching [2].
    upper, lower = X[:n], X[n:]
    return upper[:, :n], upper[:, n:], lower[:, :n], lower[:, n:]

