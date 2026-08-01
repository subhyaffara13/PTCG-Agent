
def record(event: Event, destination: str = "null") -> None:
    _get_or_create_logger(destination).info(event.serialize())


def record(
    fn: Callable[_P, _R], error_handler: ErrorHandler | None = None
) -> Callable[_P, _R | None]:
    """
    Syntactic sugar to record errors/exceptions that happened in the decorated
    function using the provided ``error_handler``.

    Using this decorator is equivalent to:

    ::

     error_handler = get_error_handler()
     error_handler.initialize()
     try:
         foobar()
     except ChildFailedError as e:
         _, failure = e.get_first_failure()
         error_handler.dump_error_file(failure.error_file, failure.exitcode)
         raise
     except Exception as e:
         error_handler.record_exception(e)
         raise

    .. important:: use this decorator once per process at the top level method,
                   typically this is the main method.

    Example

    ::

     @record
     def main():
         pass


     if __name__ == "__main__":
         main()

    """
    if not error_handler:
        error_handler = get_error_handler()

    def wrap(f: Callable[_P, _R]) -> Callable[_P, _R | None]:
        @wraps(f)
        def wrapper(*args: _P.args, **kwargs: _P.kwargs):
            if error_handler is None:
                raise AssertionError  # assertion for mypy type checker
            error_handler.initialize()
            try:
                return f(*args, **kwargs)
            except SystemExit as se:
                # For run_path based entrypoints, SystemExit with code = 0 will never exit.
                # Handling it here by returning a value:
                if se.code == 0:
                    return None
                else:
                    raise
            except ChildFailedError as e:
                rank, failure = e.get_first_failure()
                if failure.error_file != _NOT_AVAILABLE:
                    error_handler.dump_error_file(failure.error_file, failure.exitcode)
                else:
                    logger.info(
                        (
                            "local_rank %s FAILED with no error file."
                            " Decorate your entrypoint fn with @record for traceback info."
                            " See: https://pytorch.org/docs/stable/elastic/errors.html",
                            rank,
                        )
                    )
                raise
            except Exception as e:
                error_handler.record_exception(e)
                raise

        return wrapper

    return wrap(fn)

