
def whiten(obs, check_finite=None):
    """
    Normalize a group of observations on a per feature basis.

    Before running k-means, it is beneficial to rescale each feature
    dimension of the observation set by its standard deviation (i.e. "whiten"
    it - as in "white noise" where each frequency has equal power).
    Each feature is divided by its standard deviation across all observations
    to give it unit variance.

    Parameters
    ----------
    obs : ndarray
        Each row of the array is an observation.  The
        columns are the features seen during each observation::

            #        f0  f1  f2
            obs = [[ 1., 1., 1.],  #o0
                   [ 2., 2., 2.],  #o1
                   [ 3., 3., 3.],  #o2
                   [ 4., 4., 4.]]  #o3

    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
        Default: True for eager backends and False for lazy ones.

    Returns
    -------
    result : ndarray
        Contains the values in `obs` scaled by the standard deviation
        of each column.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.cluster.vq import whiten
    >>> features  = np.array([[1.9, 2.3, 1.7],
    ...                       [1.5, 2.5, 2.2],
    ...                       [0.8, 0.6, 1.7,]])
    >>> whiten(features)
    array([[ 4.17944278,  2.69811351,  7.21248917],
           [ 3.29956009,  2.93273208,  9.33380951],
           [ 1.75976538,  0.7038557 ,  7.21248917]])

    """
    xp = array_namespace(obs)
    if check_finite is None:
        check_finite = not is_lazy_array(obs)
    obs = _asarray(obs, check_finite=check_finite, xp=xp)
    std_dev = xp.std(obs, axis=0)
    zero_std_mask = std_dev == 0
    std_dev = xpx.at(std_dev, zero_std_mask).set(1.0)
    if check_finite and xp.any(zero_std_mask):
        warnings.warn("Some columns have standard deviation zero. "
                      "The values of these columns will not change.",
                      RuntimeWarning, stacklevel=2)
    return obs / std_dev

