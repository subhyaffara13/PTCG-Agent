
def from_quat(
    quat: Array,
    normalize: bool = True,
    copy: bool = True,
    *,
    scalar_first: bool = False,
) -> Array:
    xp = array_namespace(quat)
    if scalar_first:
        quat = xp.roll(quat, -1, axis=-1)
    # Normalize will always copy, so we avoid the extra copy if we normalize
    if copy and not normalize:
        quat = xp.asarray(quat, copy=True)
    if normalize:
        quat = _normalize_quaternion(quat)
    return quat

