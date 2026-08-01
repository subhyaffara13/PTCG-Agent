
def xp_swapaxes(a, axis1, axis2, xp=None):
    # Equivalent of np.swapaxes written in terms of array API
    xp = array_namespace(a) if xp is None else xp
    axes = list(range(a.ndim))
    axes[axis1], axes[axis2] = axes[axis2], axes[axis1]
    a = xp.permute_dims(a, axes)
    return a

