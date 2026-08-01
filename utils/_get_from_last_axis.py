
def _get_from_last_axis(sample, i, xp):
    if not is_array_api_strict(xp):
        return sample[..., i]

    # Equivalent to `sample[..., i]` as used in `bootstrap`. Assumes i.ndim <=2.
    if i.ndim == 2:
        sample = xp.expand_dims(sample, axis=-2)
    sample, i = _broadcast_arrays((sample, i), axis=-1, xp=xp)
    return xp.take_along_axis(sample, i, axis=-1)

