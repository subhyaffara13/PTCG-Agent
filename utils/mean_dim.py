
def mean_dim(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs["input"]
    (_, reduce_on_batch, reduce_on_ragged, reduce_on_non_batch) = _wrap_jagged_dims(
        inp.dim(),
        new_kwargs["dim"],
        "mean",
        inp._ragged_idx,
    )

    if reduce_on_ragged and not reduce_on_batch:
        if reduce_on_non_batch:
            raise AssertionError(
                "Cannot reduce on both ragged and non-batch dimensions without also reducing on batch"
            )
        # calculate an intermediate sum and leave the dim in for normalization purposes
        keepdim = new_kwargs["keepdim"]
        new_kwargs["keepdim"] = True
        intermediate_sum = _apply_reduction(
            torch.ops.aten.sum.dim_IntList, "mean", 0, **new_kwargs
        )

        # normalize by sequence lengths
        lengths = inp._lengths if inp._lengths is not None else inp._offsets.diff()
        for _ in range(intermediate_sum.dim() - 1):
            lengths = lengths.unsqueeze(-1)
        out = intermediate_sum / lengths
        if not keepdim:
            out = out.squeeze(inp._ragged_idx)
        return out

    # at this point, we're just redispatching on the values buffer
    # since we expect it to be unused, specify a weird intermediate value to
    # hopefully make errors obvious
    intermediate_value = 0.42
    return _apply_reduction(func, "mean", intermediate_value, **new_kwargs)

