
def sum_default(
    self: Tensor,
    *,
    dtype: torch.dtype | None = None,
    out: Tensor | None = None,
) -> Tensor:
    if out is None:
        return aten.sum.dim_IntList(self, [], dtype=dtype)
    else:
        return aten.sum.IntList_out(self, [], dtype=dtype, out=out)


def sum_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")

    return func(inp._values, **new_kwargs)

