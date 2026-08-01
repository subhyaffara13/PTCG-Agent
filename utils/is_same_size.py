
def is_same_size(a: Tensor, b: Tensor) -> bool:
    return a.shape == b.shape


def is_same_size(func, *args, **kwargs):
    _check_args_kwargs_length(args, kwargs, f"__torch_dispatch__, {func}", len_args=2)
    return _get_data(args[0]).is_same_size(_get_data(args[1]))

