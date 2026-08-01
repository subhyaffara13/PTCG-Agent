
def _xp_copy_to_numpy(x: Array) -> np.ndarray:
    """Copies a possibly on device array to a NumPy array.

    This function is intended only for converting alternative backend
    arrays to numpy arrays within test code, to make it easier for use
    of the alternative backend to be isolated only to the function being
    tested. `_xp_copy_to_numpy` should NEVER be used except in test code
    for the specific purpose mentioned above. In production code, attempts
    to copy device arrays to NumPy arrays should fail, or else functions
    may appear to be working on the GPU when they actually aren't.

    Parameters
    ----------
    x : array

    Returns
    -------
    ndarray
    """
    xp = array_namespace(x)
    if is_numpy(xp):
        # Just return x if it is a Python scalar without a copy attribute.
        return x.copy() if hasattr(x, "copy") else x
    if is_cupy(xp):
        return x.get()
    if is_torch(xp):
        return x.cpu().numpy()
    if is_array_api_strict(xp):
        # array api strict supports multiple devices, so need to
        # ensure x is on the cpu before copying to NumPy.
        return np.asarray(
            xp.asarray(x, device=xp.Device("CPU_DEVICE")), copy=True
        )
    # Fall back to np.asarray. This works for dask.array. It
    # currently works for jax.numpy, but hopefully JAX will make
    # the transfer guard workable enough for use in scipy tests, in
    # which case, JAX will have to be handled explicitly.
    # If new backends are added, they may require explicit handling as
    # well.
    return np.asarray(x, copy=True)

