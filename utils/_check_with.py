
def _check_with(
    error_type,
    cond: builtins.bool | SymBool,
    message: _Callable[[], str],
):  # noqa: F811
    if not isinstance(cond, (builtins.bool, SymBool)):
        raise TypeError(f"cond must be a bool, but got {type(cond)}")

    from torch.fx.experimental.symbolic_shapes import expect_true

    if expect_true(cond):
        return

    # error_type must be a subclass of Exception and not subclass of Warning
    if not issubclass(error_type, Exception) or issubclass(error_type, Warning):
        raise AssertionError(
            f"error_type must be a subclass of Exception but not Warning, got {error_type}"
        )

    if message is None:
        message_evaluated = (
            "Expected cond to be True, but got False. (Could this error "
            "message be improved? If so, please report an enhancement request "
            "to PyTorch.)"
        )

    else:
        if not callable(message):
            raise TypeError("message must be a callable")

        message_evaluated = str(message())

    raise error_type(message_evaluated)

