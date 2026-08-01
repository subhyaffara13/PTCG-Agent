
def _pretty_print_args_kwargs(*args: Any, **kwargs: Any) -> str:
    inputs_repr = ", ".join(repr(arg) for arg in args)
    kwargs_repr = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())

    all_args = []
    if inputs_repr:
        all_args.append(inputs_repr)
    if kwargs_repr:
        all_args.append(kwargs_repr)

    return ", ".join(all_args)

