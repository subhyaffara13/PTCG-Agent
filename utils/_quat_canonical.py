
def _quat_canonical(quat: Array) -> Array:
    xp = array_namespace(quat)
    mask = quat[..., 3] < 0
    zero_w = quat[..., 3] == 0
    mask = mask | (zero_w & (quat[..., 0] < 0))
    zero_wx = zero_w & (quat[..., 0] == 0)
    mask = mask | (zero_wx & (quat[..., 1] < 0))
    zero_wxy = zero_wx & (quat[..., 1] == 0)
    mask = mask | (zero_wxy & (quat[..., 2] < 0))
    return xp.where(mask[..., None], -quat, quat)

