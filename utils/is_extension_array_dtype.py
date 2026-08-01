
def is_extension_array_dtype(arr_or_dtype) -> bool:
    """
    Check if an object is a pandas extension array type.

    See the :ref:`Use Guide <extending.extension-types>` for more.

    Parameters
    ----------
    arr_or_dtype : object
        For array-like input, the ``.dtype`` attribute will
        be extracted.

    Returns
    -------
    bool
        Whether the `arr_or_dtype` is an extension array type.

    See Also
    --------
    api.extensions.ExtensionArray : Abstract base class for pandas extension arrays.

    Notes
    -----
    This checks whether an object implements the pandas extension
    array interface. In pandas, this includes:

    * Categorical
    * Sparse
    * Interval
    * Period
    * DatetimeArray
    * TimedeltaArray

    Third-party libraries may implement arrays or types satisfying
    this interface as well.

    Examples
    --------
    >>> from pandas.api.types import is_extension_array_dtype
    >>> arr = pd.Categorical(["a", "b"])
    >>> is_extension_array_dtype(arr)
    True
    >>> is_extension_array_dtype(arr.dtype)
    True

    >>> arr = np.array(["a", "b"])
    >>> is_extension_array_dtype(arr.dtype)
    False
    """
    dtype = getattr(arr_or_dtype, "dtype", arr_or_dtype)
    if isinstance(dtype, ExtensionDtype):
        return True
    elif isinstance(dtype, np.dtype):
        return False
    else:
        try:
            with warnings.catch_warnings():
                # pandas_dtype(..) can raise UserWarning for class input
                warnings.simplefilter("ignore", UserWarning)
                dtype = pandas_dtype(dtype)
        except (TypeError, ValueError):
            # np.dtype(..) can raise ValueError
            return False
        return isinstance(dtype, ExtensionDtype)

