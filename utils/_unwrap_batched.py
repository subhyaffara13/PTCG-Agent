
def _unwrap_batched(
    batched_outputs: Tensor | tuple[Tensor, ...],
    out_dims: out_dims_t,
    vmap_level: int,
    batch_size: int,
    func: Callable,
    allow_none_pass_through: bool = False,
) -> tuple:
    num_outputs = _num_outputs(batched_outputs)
    out_dims_as_tuple = _as_tuple(
        out_dims,
        num_outputs,
        lambda: f"vmap({_get_name(func)}, ..., out_dims={out_dims}): `out_dims` must "
        f"have one dim per output (got {num_outputs} outputs) of {_get_name(func)}.",
    )

    # NOTE [Ignored _remove_batch_dim, _add_batch_dim]
    # There is something wrong with our type bindings for functions that begin
    # with '_', see #40397.
    if isinstance(batched_outputs, Tensor):
        out_dim = out_dims_as_tuple[0]
        return torch._remove_batch_dim(batched_outputs, vmap_level, batch_size, out_dim)  # type: ignore[return-value]
    if allow_none_pass_through:
        return tuple(
            (
                torch._remove_batch_dim(out, vmap_level, batch_size, out_dim)
                if out is not None
                else None
            )
            for out, out_dim in zip(batched_outputs, out_dims_as_tuple)
        )
    else:
        return tuple(
            torch._remove_batch_dim(out, vmap_level, batch_size, out_dim)
            for out, out_dim in zip(batched_outputs, out_dims_as_tuple)
        )


def _unwrap_batched(
    batched_outputs: Tensor | tuple[Tensor, ...],
    out_dims: out_dims_t,
    vmap_level: int,
    batch_size: int,
    func: Callable[..., Any],
) -> tuple[Any, ...]:
    flat_batched_outputs, output_spec = tree_flatten(batched_outputs)

    def incompatible_error() -> NoReturn:
        raise ValueError(
            f"vmap({_get_name(func)}, ..., out_dims={out_dims})(<inputs>): "
            f"out_dims is not compatible with the structure of `outputs`. "
            f"out_dims has structure {tree_flatten(out_dims)[1]} but outputs "
            f"has structure {output_spec}."
        )

    flat_out_dims: list[int | None] = []
    if isinstance(batched_outputs, torch.Tensor):
        # Some weird edge case requires us to spell out the following
        # see test_out_dims_edge_case
        if isinstance(out_dims, int):
            flat_out_dims = [out_dims]
        elif isinstance(out_dims, tuple) and len(out_dims) == 1:
            flat_out_dims = list(out_dims)
        elif out_dims is None:
            flat_out_dims = [out_dims]
        else:
            incompatible_error()
    else:
        broadcast_result = _broadcast_to_and_flatten(out_dims, output_spec)
        if broadcast_result is None:
            incompatible_error()
        else:
            flat_out_dims = broadcast_result

    flat_outputs = [
        _maybe_remove_batch_dim(
            _get_name(func), batched_output, vmap_level, batch_size, out_dim
        )
        for batched_output, out_dim in zip(flat_batched_outputs, flat_out_dims)
    ]
    return tree_unflatten(flat_outputs, output_spec)

