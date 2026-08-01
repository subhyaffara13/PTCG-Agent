
def collect_thread_exception(config: Config) -> None:
    pop_thread_exception = config.stash[thread_exceptions].pop
    errors: list[pytest.PytestUnhandledThreadExceptionWarning | RuntimeError] = []
    meta = None
    hook_error = None
    try:
        while True:
            try:
                meta = pop_thread_exception()
            except IndexError:
                break

            if isinstance(meta, BaseException):
                hook_error = RuntimeError("Failed to process thread exception")
                hook_error.__cause__ = meta
                errors.append(hook_error)
                continue

            msg = meta.msg
            try:
                warnings.warn(pytest.PytestUnhandledThreadExceptionWarning(msg))
            except pytest.PytestUnhandledThreadExceptionWarning as e:
                # This except happens when the warning is treated as an error (e.g. `-Werror`).
                if meta.exc_value is not None:
                    # Exceptions have a better way to show the traceback, but
                    # warnings do not, so hide the traceback from the msg and
                    # set the cause so the traceback shows up in the right place.
                    e.args = (meta.cause_msg,)
                    e.__cause__ = meta.exc_value
                errors.append(e)

        if len(errors) == 1:
            raise errors[0]
        if errors:
            raise ExceptionGroup("multiple thread exception warnings", errors)
    finally:
        del errors, meta, hook_error

