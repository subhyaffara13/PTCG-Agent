
def restore_vmap(
    func: Callable[..., _R], in_dims: in_dims_t, batch_size: int, randomness: str
) -> Callable[..., tuple[Any, Any]]:
    def inner(*args: Any, **kwargs: Any) -> tuple[Any, Any]:
        with vmap_increment_nesting(batch_size, randomness) as vmap_level:
            batched_inputs = wrap_batched(args, in_dims, vmap_level)
            batched_outputs = func(*batched_inputs, **kwargs)
            return unwrap_batched(batched_outputs, vmap_level)

    return inner

