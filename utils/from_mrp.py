
def from_mrp(mrp: Array) -> Array:
    xp = array_namespace(mrp)
    if mrp.shape[-1] != 3:
        raise ValueError(f"Expected `mrp` to have shape (..., 3), got {mrp.shape}")
    mrp2_plus_1 = xp.linalg.vecdot(mrp, mrp, axis=-1)[..., None] + 1
    q_no_norm = xp.concat([2 * mrp[..., :3], (2 - mrp2_plus_1)], axis=-1)
    quat = q_no_norm / mrp2_plus_1
    return quat

