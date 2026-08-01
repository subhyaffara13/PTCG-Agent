
def conv_args_and_kwargs(kwarg_names, expanded_args_and_kwargs):
    args = expanded_args_and_kwargs[: len(expanded_args_and_kwargs) - len(kwarg_names)]
    kwargs = expanded_args_and_kwargs[
        len(expanded_args_and_kwargs) - len(kwarg_names) :
    ]
    kwargs = dict(zip(kwarg_names, kwargs, strict=True))

    return conv_normalizer(*args, **kwargs)

