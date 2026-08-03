import functools

def _sticky_export(
    forward_func: typing.Callable[_InputT, _RetT],
    dynamic_shapes_callback: typing.Callable[
        _InputT, list[typing.Any] | dict[str, typing.Any] | tuple[typing.Any, ...]
    ]
    | None = None,
) -> typing.Callable[_InputT, _RetT]:
    """
    Lazily export the model on first forward call.
    Usage:
        model.forward = _sticky_export(model.forward, dynamic_shapes_callback=callback)
    """
    model = forward_func.__self__  # type: ignore[attr-defined]
    original_forward = forward_func.__func__  # type: ignore[attr-defined]

    @functools.wraps(forward_func)
    def wrapper(*args: _InputT.args, **kwargs: _InputT.kwargs) -> _RetT:
        # Unpatch forward to avoid recursion during export
        model.forward = types.MethodType(original_forward, model)

        dynamic_shapes_spec = None
        if dynamic_shapes_callback:
            dynamic_shapes_spec = dynamic_shapes_callback(*args, **kwargs)

        try:
            exported = torch.export.export(
                model,
                args,
                kwargs,
                dynamic_shapes=dynamic_shapes_spec,
            ).module()
            wrapper._exported_artifact = exported  # type: ignore[attr-defined]
        finally:
            # Restore the wrapper after export
            model.forward = wrapper

        return exported(*args, **kwargs)

    return wrapper

