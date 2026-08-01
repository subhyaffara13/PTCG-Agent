
def reraise(error):
    """Return a function that raises the given error when evaluated"""

    def local_function(*args, **kwargs):
        raise error

    return local_function


def reraise(
    tp: type[BaseException] | None,
    value: BaseException,
    tb: TracebackType | None = None,
) -> typing.NoReturn:
    try:
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    finally:
        value = None  # type: ignore[assignment]
        tb = None


def reraise(
    tp: type[BaseException] | None,
    value: BaseException,
    tb: TracebackType | None = None,
) -> typing.NoReturn:
    try:
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
    finally:
        value = None  # type: ignore[assignment]
        tb = None


def reraise(
    e: Exception,
    prefix: Optional[_Str] = None,
    suffix: Optional[_Str] = None,
) -> NoReturn:
  """Reraise an exception with an additional message.

  Benefit: Contrary to `raise ... from ...` and
  `raise Exception().with_traceback(tb)`, this function will:

  * Keep the original exception type, attributes,...
  * Avoid multi-nested `During handling of the above exception, another
    exception occurred`. Only the single original stacktrace is displayed.

  This result in cleaner and more compact error messages.

  Usage:

  ```
  try:
    fn(x)
  except Exception as e:
    epy.reraise(e, prefix=f'Error for {x}: ')
  ```

  Args:
    e: Exception to reraise
    prefix: Prefix to add to the exception message.
    suffix: Suffix to add to the exception message.
  """
  # TODO(epot): Mutate the `e.__traceback__` when not in IPython.
  # Hide the function from the traceback. Is supported by Pytest and IPython 7
  __tracebackhide__ = True  # pylint: disable=unused-variable,invalid-name

  new_exception = wrap_error(e, prefix=prefix, suffix=suffix)

  # Propagate the exception:
  # * `with_traceback` will propagate the original stacktrace
  # * `from e.__cause__` will:
  #   * Propagate the original `__cause__` (likely `None`)
  #   * Set `__suppress_context__` to True, so `__context__` isn't displayed
  #     This avoid multiple `During handling of the above exception, another
  #     exception occurred:` messages when nesting `reraise`
  raise new_exception from new_exception.__cause__

