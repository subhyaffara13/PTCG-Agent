
def sorted_svd(m, k, which='LM'):
    # Compute svd of a dense matrix m, and return singular vectors/values
    # sorted.
    if issparse(m):
        m = m.toarray()
    u, s, vh = svd(m)
    if which == 'LM':
        ii = np.argsort(s)[-k:]
    elif which == 'SM':
        ii = np.argsort(s)[:k]
    else:
        raise ValueError(f"unknown which={which!r}")

    return u[:, ii], s[ii], vh[ii]

