
def _disable_dynamo_if_unsupported(
    single_tensor_fn: Callable[..., object] | None = None,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    # workaround for torchscript BC
    # it requires all called functions to be in the
    # global environment at the site at which the
    # maybe_fallback closure is created
    if single_tensor_fn:
        globals()[single_tensor_fn.__name__] = single_tensor_fn

    def wrapper(func: Callable[_P, _T]) -> Callable[_P, _T]:
        import inspect

        disabled_func = torch._disable_dynamo(func)
        ps = inspect.signature(func).parameters
        has_state_steps = True
        try:
            state_steps_ind = list(ps.keys()).index("state_steps")
        except ValueError:
            has_state_steps = False

        # Today, there are cases where we stack state steps
        # and pass them as the value arg of foreach ops.
        # Having state steps on cuda as the value arg is not supported in eager,
        # but this only occurs in the rare case that the user explicitly deletes
        # the capturable flag. If capturable=True, this is not a problem.
        @functools.wraps(func)
        def maybe_fallback(*args: _P.args, **kwargs: _P.kwargs):
            if torch.compiler.is_compiling() and (
                not kwargs.get("capturable", False)
                and has_state_steps
                and (arg := args[state_steps_ind])
                and isinstance(arg, Sequence)
                and arg[0].is_cuda
                or (
                    "state_steps" in kwargs
                    and (kwarg := kwargs["state_steps"])
                    and isinstance(kwarg, Sequence)
                    and kwarg[0].is_cuda
                )
            ):
                return disabled_func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return maybe_fallback

    return wrapper

