
def _function_where(func, *args, **kwargs):
    _check_args_kwargs_length(
        args, kwargs, "__torch_function__, torch.where", len_args=3, len_kwargs=0
    )
    return _MaskedWhere.apply(*args)

