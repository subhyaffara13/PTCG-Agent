
def rotation_to_xp(r: Rotation, xp):
    dtype = xpx.default_dtype(xp)
    return Rotation.from_quat(xp.asarray(r.as_quat(), dtype=dtype))


def rotation_to_xp(r: Rotation, xp):
    dtype = xpx.default_dtype(xp)
    return Rotation.from_quat(xp.asarray(r.as_quat(), dtype=dtype))

