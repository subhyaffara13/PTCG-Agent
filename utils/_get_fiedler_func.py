
def _get_fiedler_func(method):
    """Returns a function that solves the Fiedler eigenvalue problem."""
    import numpy as np

    if method == "tracemin":  # old style keyword <v2.1
        method = "tracemin_pcg"
    if method in ("tracemin_pcg", "tracemin_lu"):

        def find_fiedler(L, x, normalized, tol, seed):
            q = 1 if method == "tracemin_pcg" else min(4, L.shape[0] - 1)
            X = np.asarray(seed.normal(size=(q, L.shape[0]))).T
            sigma, X = _tracemin_fiedler(L, X, normalized, tol, method)
            return sigma[0], X[:, 0]

    elif method == "lanczos" or method == "lobpcg":

        def find_fiedler(L, x, normalized, tol, seed):
            import scipy as sp

            L = sp.sparse.csc_array(L, dtype=float)
            n = L.shape[0]
            if normalized:
                D = sp.sparse.dia_array(
                    (1.0 / np.sqrt(L.diagonal()), 0), shape=(n, n)
                ).tocsc()
                L = D @ L @ D
            if method == "lanczos" or n < 10:
                # Avoid LOBPCG when n < 10 due to
                # https://github.com/scipy/scipy/issues/3592
                # https://github.com/scipy/scipy/pull/3594
                sigma, X = sp.sparse.linalg.eigsh(
                    L, 2, which="SM", tol=tol, return_eigenvectors=True
                )
                return sigma[1], X[:, 1]
            else:
                X = np.asarray(np.atleast_2d(x).T)
                M = sp.sparse.dia_array((1.0 / L.diagonal(), 0), shape=(n, n)).tocsr()
                Y = np.ones(n)
                if normalized:
                    Y /= D.diagonal()
                sigma, X = sp.sparse.linalg.lobpcg(
                    L, X, M=M, Y=np.atleast_2d(Y).T, tol=tol, maxiter=n, largest=False
                )
                return sigma[0], X[:, 0]

    else:
        raise nx.NetworkXError(f"unknown method {method!r}.")

    return find_fiedler

