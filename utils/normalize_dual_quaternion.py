
def normalize_dual_quaternion(dual_quat: ArrayLike) -> Array:
    """Normalize dual quaternion."""
    xp = array_namespace(dual_quat)
    dual_quat = _promote(dual_quat, xp=xp)
    single = dual_quat.ndim == 1 and is_numpy(xp)
    if single:
        dual_quat = xpx.atleast_nd(dual_quat, ndim=2, xp=xp)
    cython_compatible = dual_quat.ndim < 3
    dq = select_backend(xp, cython_compatible).normalize_dual_quaternion(dual_quat)
    if single:
        return dq[0]
    return dq


def normalize_dual_quaternion(dual_quat: Array) -> Array:
    """Normalize dual quaternion."""
    xp = array_namespace(dual_quat)
    real, dual = _normalize_dual_quaternion(dual_quat[..., :4], dual_quat[..., 4:])
    return xp.concat((real, dual), axis=-1)

