
def _promote(*args: ArrayLike, xp: ModuleType) -> Array:
    """Promote arrays to float64 for numpy, else according to the Array API spec.

    The return array dtype follows the following rules:
    - If quat is an ArrayLike or NumPy array, we always promote to float64
    - If quat is an Array from frameworks other than NumPy, we preserve the precision
      of the input array dtype.

    The first rule is required by the cython backend signatures that expect
    cython.double views. The second rule is necessary to promote non-floating arrays
    to the correct type in frameworks that may not support double precision (e.g.
    jax by default).
    """
    if is_numpy(xp):
        args += (np.empty(0, dtype=np.float64),)  # Force float64 conversion
        out = xp_promote(*args, force_floating=True, xp=xp)
        if len(args) == 2:  # One argument was passed  + the added empty array
            return out[0]
        return out[:-1]
    return xp_promote(*args, force_floating=True, xp=xp)

