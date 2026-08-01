
def _values(func, *args, **kwargs):
    _check_args_kwargs_length(
        args, kwargs, f"__torch_dispatch__, {func}", len_args=1, len_kwargs=0
    )
    data = _get_data(args[0]).values()
    return MaskedTensor(data, torch.ones_like(data).bool())

