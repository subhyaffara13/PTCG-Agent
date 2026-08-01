
def _maybe_remove_batch_dim(
    name: str,
    batched_output: Any,
    vmap_level: int,
    batch_size: int,
    out_dim: int | None,
) -> torch.Tensor:
    if out_dim is None:
        if isinstance(batched_output, torch.Tensor) and is_batchedtensor(
            batched_output
        ):
            raise ValueError(
                f"vmap({name}, ...): `{name}` can not return a "
                f"BatchedTensor when out_dim is None"
            )
        return batched_output

    # out_dim is non None
    if not isinstance(batched_output, torch.Tensor):
        raise ValueError(
            f"vmap({name}, ...): `{name}` must only return "
            f"Tensors, got type {type(batched_output)}. "
            "Did you mean to set out_dims= to None for output?"
        )

    return _remove_batch_dim(batched_output, vmap_level, batch_size, out_dim)

