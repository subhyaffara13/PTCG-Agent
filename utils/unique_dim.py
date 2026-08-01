
def unique_dim(
    fake_mode: FakeTensorMode,
    func: OpOverload,
    arg: FakeTensor,
    dim: int,
    sorted: bool = True,
    return_inverse: bool = False,
    return_counts: bool = False,
) -> tuple[FakeTensor, FakeTensor, FakeTensor]:
    return _unique(
        fake_mode,
        func,
        arg,
        # normalize dim to be non-negative
        dim if dim >= 0 else dim % max(arg.ndim, 1),
        sorted,
        return_inverse,
        return_counts,
    )


def unique_dim(
    g: jit_utils.GraphContext, self, dim, sorted, return_inverse, return_counts
):
    u, _indices, inverse_indices, counts = g.op(
        "Unique", self, axis_i=dim, sorted_i=sorted, outputs=4
    )
    return u, inverse_indices, counts

