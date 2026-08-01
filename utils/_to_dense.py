
def _to_dense(func, *args, **kwargs):
    _check_args_kwargs_length(
        args, kwargs, f"__torch_dispatch__, {func}", len_args=1, len_kwargs=0
    )
    if not torch.is_tensor(args[0]):
        raise ValueError(f"__torch_dispatch__, {func}: expected args[0] to be a tensor")
    mt = args[0]
    if not is_masked_tensor(mt):
        mt = MaskedTensor(mt, torch.ones_like(mt).bool())
    new_data = func(_get_data(args[0]))
    new_mask = func(_maybe_get_mask(args[0]))
    return MaskedTensor(new_data, new_mask)

