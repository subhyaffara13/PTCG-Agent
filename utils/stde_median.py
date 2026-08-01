
def stde_median(data, axis=None):
    """Returns the McKean-Schrader estimate of the standard error of the sample
    median along the given axis. masked values are discarded.

    Parameters
    ----------
    data : ndarray
        Data to trim.
    axis : {None,int}, optional
        Axis along which to perform the trimming.
        If None, the input array is first flattened.

    """
    def _stdemed_1D(data):
        data = np.sort(data.compressed())
        n = len(data)
        z = 2.5758293035489004
        k = int(np.round((n+1)/2. - z * np.sqrt(n/4.),0))
        return ((data[n-k] - data[k-1])/(2.*z))

    data = ma.array(data, copy=False, subok=True)
    if (axis is None):
        return _stdemed_1D(data)
    else:
        if data.ndim > 2:
            raise ValueError(f"Array 'data' must be at most two dimensional, "
                             f"but got data.ndim = {data.ndim}")
        return ma.apply_along_axis(_stdemed_1D, axis, data)

