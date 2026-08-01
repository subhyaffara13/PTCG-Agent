
def raise_observed_exception(
    exc_type: type[Exception],
    tx: InstructionTranslatorBase,
    *,
    args: list[VariableTracker] | list[str] | None = None,
    kwargs: dict[str, VariableTracker] | None = None,
) -> NoReturn:
    from .symbolic_convert import ExceptionVals
    from .variables.builder import SourcelessBuilder

    if args:
        args_ = [
            SourcelessBuilder.create(tx, arg) if isinstance(arg, str) else arg
            for arg in args
        ]
    else:
        args_: list[VariableTracker] = []

    # CPython here raises an exception. Since there is no python code, we have to manually setup the exception
    # stack and raise the exception.
    exception_vt = SourcelessBuilder.create(tx, exc_type).call_function(
        tx, args_, kwargs or {}
    )
    assert isinstance(exception_vt, ExceptionVals)
    tx._attach_traceback_to_exception(exception_vt)
    tx.exn_vt_stack.set_current_exception(exception_vt)  # type: ignore[arg-type]
    raised_exc = get_dynamo_observed_exception(exc_type)
    # Store the original exception arguments for better error messages
    if args:
        raise raised_exc(*args_)
    raise raised_exc

