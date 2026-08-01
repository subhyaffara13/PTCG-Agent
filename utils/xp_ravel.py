
def xp_ravel(x: Array, /, *, xp: ModuleType | None = None) -> Array:
    # Equivalent of np.ravel written in terms of array API
    # Even though it's one line, it comes up so often that it's worth having
    # this function for readability
    xp = array_namespace(x) if xp is None else xp
    return xp.reshape(x, (-1,))

