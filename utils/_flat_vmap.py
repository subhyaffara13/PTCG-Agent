
def _flat_vmap(
    func: Callable[..., Tensor | tuple[Tensor, ...]],
    batch_size: int,
    flat_in_dims: list[int | None],
    flat_args: list[Any],
    args_spec: TreeSpec,
    out_dims: out_dims_t,
    randomness: str,
    **kwargs: Any,
) -> Any:
    with vmap_increment_nesting(batch_size, randomness) as vmap_level:
        batched_inputs = _create_batched_inputs(
            flat_in_dims, flat_args, vmap_level, args_spec
        )
        batched_outputs = func(*batched_inputs, **kwargs)
        return _unwrap_batched(batched_outputs, out_dims, vmap_level, batch_size, func)

