
def _create_oneof_shared_memory(space: OneOf, n: int = 1, ctx=mp):
    return (ctx.Array(np.dtype(np.int64).char, n),) + tuple(
        create_shared_memory(subspace, n=n, ctx=ctx) for subspace in space.spaces
    )

