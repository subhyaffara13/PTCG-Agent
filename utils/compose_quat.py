
def compose_quat(p: Array, q: Array) -> Array:
    xp = array_namespace(p)
    cross = xp.linalg.cross(p[..., :3], q[..., :3])
    qx = p[..., 3] * q[..., 0] + q[..., 3] * p[..., 0] + cross[..., 0]
    qy = p[..., 3] * q[..., 1] + q[..., 3] * p[..., 1] + cross[..., 1]
    qz = p[..., 3] * q[..., 2] + q[..., 3] * p[..., 2] + cross[..., 2]
    qw = (
        p[..., 3] * q[..., 3]
        - p[..., 0] * q[..., 0]
        - p[..., 1] * q[..., 1]
        - p[..., 2] * q[..., 2]
    )
    quat = xp.stack([qx, qy, qz, qw], axis=-1)
    return quat

