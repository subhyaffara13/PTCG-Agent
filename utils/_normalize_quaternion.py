
def _normalize_quaternion(quat: Array) -> Array:
    xp = array_namespace(quat)
    quat_norm = xp_vector_norm(quat, axis=-1, keepdims=True, xp=xp)
    zero_norm = quat_norm == 0
    if is_lazy_array(quat_norm):
        quat = xp.where(zero_norm, xp.nan, quat)
    elif xp.any(zero_norm):
        raise ValueError("Found zero norm quaternions in `quat`.")
    return quat / quat_norm


def _normalize_quaternion(quat: Array) -> Array:
  return quat / _vector_norm(quat)

