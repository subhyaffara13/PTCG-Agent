
def rigid_transform_to_xp(r: RigidTransform, xp):
    dtype = xpx.default_dtype(xp)
    return RigidTransform.from_matrix(xp.asarray(r.as_matrix(), dtype=dtype))

