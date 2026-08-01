
def _get_data_scale(X, Y, Z):
    """
    Estimate the scale of the 3D data for use in depth shading

    Parameters
    ----------
    X, Y, Z : masked arrays
        The data to estimate the scale of.
    """
    # Account for empty datasets. Assume that X Y and Z have the same number
    # of elements.
    if not np.ma.count(X):
        return 0

    # Estimate the scale using the RSS of the ranges of the dimensions
    # Note that we don't use np.ma.ptp() because we otherwise get a build
    # warning about handing empty arrays.
    ptp_x = X.max() - X.min()
    ptp_y = Y.max() - Y.min()
    ptp_z = Z.max() - Z.min()
    return np.sqrt(ptp_x ** 2 + ptp_y ** 2 + ptp_z ** 2)

