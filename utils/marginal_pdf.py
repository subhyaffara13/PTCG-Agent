
def marginal_pdf(X, X_ndim, dimensions, x):
    """Integrate marginalized dimensions of multivariate
    probability distribution to calculate the marginalized
    distribution.
    """
    # Sort input data based on order of dimensions
    dimensions = np.asarray(dimensions)
    dimensions[dimensions < 0] += X_ndim
    dim_sort_idx = dimensions.argsort()
    x = x[:, dim_sort_idx]

    i_marginalize = np.ones(X_ndim, dtype=bool)
    i_marginalize[dimensions] = False

    def g(z):
        y = np.empty((z.shape[0], x.shape[0], X_ndim))
        y[..., i_marginalize] = z[:, np.newaxis, :]
        y[..., ~i_marginalize] = x
        return X.pdf(y)

    inf = np.full(X_ndim - len(dimensions), np.inf)
    return cubature(g, -inf, inf).estimate

