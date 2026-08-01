
def _is_any_true(func, *args, **kwargs):
    _check_args_kwargs_length(
        args, kwargs, f"__torch_dispatch__, {func}", len_args=1, len_kwargs=0
    )
    data = _get_data(args[0])
    mask = _maybe_get_mask(args[0])
    if mask is None:
        raise ValueError(
            f"__torch_dispatch__, {func}: expected args[0] to be a MaskedTensor"
        )
    if data.dtype != torch.bool:
        raise ValueError(f"__torch_dispatch__, {func}: expected a boolean tensor")
    if data.is_sparse:
        raise ValueError(f"MaskedTensors with sparse data do not have {func}")

    return MaskedTensor(func(data & mask), torch.tensor(True))

