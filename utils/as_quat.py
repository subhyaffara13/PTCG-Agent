
def as_quat(
    quat: Array, canonical: bool = False, *, scalar_first: bool = False
) -> Array:
    xp = array_namespace(quat)
    if canonical:
        quat = _quat_canonical(quat)
    if scalar_first:
        quat = xp.roll(quat, 1, axis=-1)
    return quat

