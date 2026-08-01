
def _lerp(a, b, t, out=None):
    """
    Compute the linear interpolation weighted by gamma on each point of
    two same shape array.

    a : array_like
        Left bound.
    b : array_like
        Right bound.
    t : array_like
        The interpolation weight.
    out : array_like
        Output array.
    """
    diff_b_a = b - a
    lerp_interpolation = add(a, diff_b_a * t, out=... if out is None else out)
    subtract(b, diff_b_a * (1 - t), out=lerp_interpolation, where=t >= 0.5,
             casting='unsafe', dtype=type(lerp_interpolation.dtype))
    if lerp_interpolation.ndim == 0 and out is None:
        lerp_interpolation = lerp_interpolation[()]  # unpack 0d arrays
    return lerp_interpolation

