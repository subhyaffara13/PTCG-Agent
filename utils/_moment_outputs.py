
def _moment_outputs(kwds, default_order=1):
    order = np.atleast_1d(kwds.get('order', default_order))
    message = "`order` must be a scalar or a non-empty 1D array."
    if order.size == 0 or order.ndim > 1:
        raise ValueError(message)
    return len(order)

