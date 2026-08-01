
def from_translation(translation: Array) -> Array:
    xp = array_namespace(translation)

    if translation.shape[-1] != 3:
        raise ValueError(
            f"Expected `translation` to have shape (..., 3), got {translation.shape}."
        )
    device = xp_device(translation)
    dtype = xp_result_type(translation, force_floating=True, xp=xp)
    eye = xp.eye(4, dtype=dtype, device=device)

    matrix = xpx.atleast_nd(eye, ndim=translation.ndim + 1, xp=xp)
    matrix = xp.zeros(
        (*translation.shape[:-1], 4, 4),
        dtype=dtype,
        device=device,
    )
    matrix = xpx.at(matrix)[...].set(xp.eye(4, dtype=dtype, device=device))
    matrix = xpx.at(matrix)[..., :3, 3].set(
        xp_promote(translation, force_floating=True, xp=xp)
    )
    return matrix

