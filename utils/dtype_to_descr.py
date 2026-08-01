
def dtype_to_descr(dtype):
    """
    Get a serializable descriptor from the dtype.

    The .descr attribute of a dtype object cannot be round-tripped through
    the dtype() constructor. Simple types, like dtype('float32'), have
    a descr which looks like a record array with one field with '' as
    a name. The dtype() constructor interprets this as a request to give
    a default name.  Instead, we construct descriptor that can be passed to
    dtype().

    Parameters
    ----------
    dtype : dtype
        The dtype of the array that will be written to disk.

    Returns
    -------
    descr : object
        An object that can be passed to `numpy.dtype()` in order to
        replicate the input dtype.

    """
    # NOTE: that drop_metadata may not return the right dtype e.g. for user
    #       dtypes.  In that case our code below would fail the same, though.
    new_dtype = drop_metadata(dtype)
    if new_dtype is not dtype:
        warnings.warn("metadata on a dtype is not saved to an npy/npz. "
                      "Use another format (such as pickle) to store it.",
                      UserWarning, stacklevel=2)
    dtype = new_dtype

    if dtype.names is not None:
        # This is a record array. The .descr is fine.  XXX: parts of the
        # record array with an empty name, like padding bytes, still get
        # fiddled with. This needs to be fixed in the C implementation of
        # dtype().
        return dtype.descr
    elif not type(dtype)._legacy:
        # this must be a user-defined dtype since numpy does not yet expose any
        # non-legacy dtypes in the public API
        #
        # non-legacy dtypes don't yet have __array_interface__
        # support. Instead, as a hack, we use pickle to save the array, and lie
        # that the dtype is object. When the array is loaded, the descriptor is
        # unpickled with the array and the object dtype in the header is
        # discarded.
        #
        # a future NEP should define a way to serialize user-defined
        # descriptors and ideally work out the possible security implications
        warnings.warn("Custom dtypes are saved as python objects using the "
                      "pickle protocol. Loading this file requires "
                      "allow_pickle=True to be set.",
                      UserWarning, stacklevel=2)
        return "|O"
    else:
        return dtype.str

