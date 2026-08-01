
def scatter_fallback(
    op_overload: torch._ops.OpOverload,
    self,
    dim: int,
    index,
    src,
    *,
    reduce: str | None = None,
    include_self: bool = True,
):
    src_is_tensor = isinstance(src, TensorBox)
    if use_scatter_fallback(
        op_overload,
        reduce,
        self.get_dtype(),
        cast(torch.dtype, src.get_dtype() if src_is_tensor else type(src)),
        # pyrefly: ignore [missing-attribute]
        src.get_device().type if src_is_tensor else "not impl",
        src_is_tensor,
    ):
        ir.ScatterFallback(
            op_overload,
            self,
            dim,
            index,
            src,
            reduce=reduce,
            include_self=include_self,
        )
        return self

    return None

