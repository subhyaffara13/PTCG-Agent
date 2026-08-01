
def detrend_signature(data, axis=1, type='linear', bp=0, *args, **kwds):
    xp = array_namespace(data)
    # JAX doesn't accept JAX arrays for bp, only ints, lists and NumPy
    # arrays.
    return xp if is_jax(xp) else array_namespace(data, bp)

