
def _handle_exception(
    *, numa_options: NumaOptions, logger_kwargs: dict[str, object]
) -> None:
    signpost_event(
        category="numa_binding",
        name="apply_exception",
        parameters={
            **logger_kwargs,
            "traceback": traceback.format_exc(),
        },
    )
    logger.exception("Failed to apply NUMA binding for input=%r", logger_kwargs)
    if numa_options.should_fall_back_if_binding_fails:
        logger.warning(
            "Continuing executing without applying NUMA binding, despite exception %s",
            traceback.format_exc(),
        )
        return
    # This function is called within an except block, so silence the warning
    # about raise without an exception.
    raise  # noqa: PLE0704


def _handle_exception(result):
    if isinstance(result, RemoteException):
        exception_msg = result.msg.encode("utf-8").decode("unicode_escape")
        # We wrap exception re-creation here in case some exception classes
        # cannot be constructed directly from a string.
        exc = None
        try:
            exc = result.exception_type(exception_msg)
        except BaseException as e:  # noqa: B036
            raise RuntimeError(  # noqa: B904
                f"Failed to create original exception type. Error msg was {str(e)}"
                f" Original exception on remote side was {exception_msg}"
            ) from e

        if exc is not None:
            raise exc

