
def _log_softmax_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    if isinstance(new_kwargs["dim"], tuple):
        raise RuntimeError(
            "log_softmax(): not supported for dimensions of type 'tuple' for NestedTensor"
        )

    inp = new_kwargs.pop("input")

    (
        new_kwargs["dim"],
        reduce_on_batch,
        reduce_on_ragged,
        _reduce_on_non_batch,
    ) = _wrap_jagged_dims(
        inp.dim(), (new_kwargs["dim"],), "log_softmax", inp._ragged_idx
    )

    if reduce_on_batch:
        raise RuntimeError(
            "log_softmax(): not supported when reducing across the batch dimension for NestedTensor"
        )

    if reduce_on_ragged:
        raise RuntimeError(
            "log_softmax(): not supported when reducing along the ragged dimension for NestedTensor"
        )

    # torch.log_softmax takes in the reduction dimension as an integer
    new_kwargs["dim"] = new_kwargs["dim"][0]

    return NestedTensor(func(inp._values, **new_kwargs), **extract_kwargs(inp))

