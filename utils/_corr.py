
def _corr(X, M):
    # Correlation coefficient r, simplified and vectorized as we need it.
    # See [7] Equation (2). Lemma 1/2 are only for distributions symmetric
    # about 0.
    Xm = X.mean(axis=-1, keepdims=True)
    Mm = M.mean(axis=-1, keepdims=True)
    num = np.sum((X - Xm) * (M - Mm), axis=-1)
    den = np.sqrt(np.sum((X - Xm)**2, axis=-1) * np.sum((M - Mm)**2, axis=-1))
    return num/den

