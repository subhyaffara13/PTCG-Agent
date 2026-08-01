
def cumulative_simpson_nd_reference(y, *, x=None, dx=None, initial=None, axis=-1):
    # Use cumulative_trapezoid if length of y < 3
    if y.shape[axis] < 3:
        if initial is None:
            return cumulative_trapezoid(y, x=x, dx=dx, axis=axis, initial=None)
        else:
            return initial + cumulative_trapezoid(y, x=x, dx=dx, axis=axis, initial=0)

    # Ensure that working axis is last axis
    y = np.moveaxis(y, axis, -1)
    x = np.moveaxis(x, axis, -1) if np.ndim(x) > 1 else x
    dx = np.moveaxis(dx, axis, -1) if np.ndim(dx) > 1 else dx
    initial = np.moveaxis(initial, axis, -1) if np.ndim(initial) > 1 else initial

    # If `x` is not present, create it from `dx`
    n = y.shape[-1]
    x = dx * np.arange(n) if dx is not None else x
    # Similarly, if `initial` is not present, set it to 0
    initial_was_none = initial is None
    initial = 0 if initial_was_none else initial

    # `np.apply_along_axis` accepts only one array, so concatenate arguments
    x = np.broadcast_to(x, y.shape)
    initial = np.broadcast_to(initial, y.shape[:-1] + (1,))
    z = np.concatenate((y, x, initial), axis=-1)

    # Use `np.apply_along_axis` to compute result
    def f(z):
        return cumulative_simpson(z[:n], x=z[n:2*n], initial=z[2*n:])
    res = np.apply_along_axis(f, -1, z)

    # Remove `initial` and undo axis move as needed
    res = res[..., 1:] if initial_was_none else res
    res = np.moveaxis(res, -1, axis)
    return res

