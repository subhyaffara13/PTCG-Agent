
def _weights_are_valid(weights, a, axis):
    """Validate weights array.

    We assume, weights is not None.
    """
    wgt = np.asanyarray(weights)

    # Sanity checks
    if a.shape != wgt.shape:
        if axis is None:
            raise TypeError(
                "Axis must be specified when shapes of a and weights "
                "differ.")
        if wgt.shape != tuple(a.shape[ax] for ax in axis):
            raise ValueError(
                "Shape of weights must be consistent with "
                "shape of a along specified axis.")

        # setup wgt to broadcast along axis
        wgt = wgt.transpose(np.argsort(axis))
        wgt = wgt.reshape(tuple((s if ax in axis else 1)
                                for ax, s in enumerate(a.shape)))
    return wgt

