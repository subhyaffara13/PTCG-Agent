from typing import Any, Callable

def _chunked_vmap(
    func: Callable[_P, Tensor | tuple[Tensor, ...]],
    flat_in_dims: list[int | None],
    chunks_flat_args: Iterable[tuple[Any, ...]],
    args_spec: TreeSpec,
    out_dims: out_dims_t,
    randomness: str,
    **kwargs: Any,
) -> Any:
    chunks_output: list[Any] = []
    rs = torch.get_rng_state() if randomness == "same" else None
    for flat_args_tuple in chunks_flat_args:
        flat_args = list(flat_args_tuple)
        batch_size = _validate_and_get_batch_size(flat_in_dims, flat_args)

        # The way we compute split the input in `_get_chunked_inputs`,
        # we may get a tensor with `0` batch-size. We skip any computation
        # in that case.
        # Eg.
        # >>> chunk_size = 1
        # >>> batch_size = 6
        # >>> t = torch.zeros(batch_size, 1)
        # >>> t.tensor_split([1, 2, 3, 4, 5, 6])
        # (tensor([[0.]]), tensor([[0.]]), tensor([[0.]]), tensor([[0.]]),
        #  tensor([[0.]]), tensor([[0.]]), tensor([], size=(0, 1)))
        if batch_size == 0:
            continue

        if rs is not None:
            torch.set_rng_state(rs)
        chunks_output.append(
            _flat_vmap(
                func,
                batch_size,
                flat_in_dims,
                flat_args,
                args_spec,
                out_dims,
                randomness,
                **kwargs,
            )
        )

    flat_output_chunks, arg_spec = _flatten_chunks_output(chunks_output)

    # chunked output tensors are held by both `flat_output_chunks` and `chunks_output`.
    # eagerly remove the reference from `chunks_output`.
    del chunks_output

    # concat chunks on out_dim
    # Note: We use cast since flat_output_chunks is modified in _concat_chunked_outputs
    # to set elements to None after processing
    flat_output = _concat_chunked_outputs(
        out_dims, arg_spec, cast(list[tuple[Any, ...] | None], flat_output_chunks)
    )

    # finally unflatten the output
    return tree_unflatten(flat_output, arg_spec)

