from typing import Any, Callable

def vmap_impl(
    func: Callable[_P, Tensor | tuple[Tensor, ...]],
    in_dims: in_dims_t,
    out_dims: out_dims_t,
    randomness: str,
    chunk_size: int | None,
    *args: _P.args,
    **kwargs: _P.kwargs,
) -> Any:
    lazy_load_decompositions()
    _check_out_dims_is_int_or_int_pytree(out_dims, func)
    batch_size, flat_in_dims, flat_args, args_spec = _process_batched_inputs(
        in_dims, args, func
    )

    if chunk_size is not None:
        chunks_flat_args = _get_chunked_inputs(
            flat_args, flat_in_dims, batch_size, chunk_size
        )
        return _chunked_vmap(
            func,
            flat_in_dims,
            chunks_flat_args,
            args_spec,
            out_dims,
            randomness,
            **kwargs,
        )

    # If chunk_size is not specified.
    return _flat_vmap(
        func,
        batch_size,
        flat_in_dims,
        flat_args,
        args_spec,
        out_dims,
        randomness,
        **kwargs,
    )

