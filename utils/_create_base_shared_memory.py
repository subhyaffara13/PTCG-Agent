
def _create_base_shared_memory(
    space: Box | Discrete | MultiDiscrete | MultiBinary, n: int = 1, ctx=mp
):
    assert space.dtype is not None
    dtype = space.dtype.char
    if dtype in "?":
        dtype = c_bool
    return ctx.Array(dtype, n * int(np.prod(space.shape)))


def _create_base_shared_memory(space, n: int = 1, ctx=mp):
    dtype = space.dtype.char
    if dtype in "?":
        dtype = c_bool
    return ctx.Array(dtype, n * int(np.prod(space.shape)))

