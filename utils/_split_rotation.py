
def _split_rotation(q: Array, xp) -> tuple[Array, Array]:
    q = xpx.atleast_nd(q, ndim=2, xp=xp)
    return q[..., -1], q[..., :-1]

