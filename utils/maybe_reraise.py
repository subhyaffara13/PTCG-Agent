from typing import Optional

def maybe_reraise(
    prefix: Optional[_Str] = None,
    suffix: Optional[_Str] = None,
) -> Iterator[None]:
  """Context manager which reraise exceptions with an additional message.

  Benefit: Contrary to `raise ... from ...` and
  `raise Exception().with_traceback(tb)`, this function will:

  * Keep the original exception type, attributes,...
  * Avoid multi-nested `During handling of the above exception, another
    exception occurred`. Only the single original stacktrace is displayed.

  This result in cleaner and more compact error messages.

  Usage:

  ```python
  with epy.maybe_reraise(prefix=f'Error for {x}:'):
    fn(x)
  ```

  Args:
    prefix: Prefix to add to the exception message. Can be a function for
      lazy-evaluation.
    suffix: Suffix to add to the exception message. Can be a function for
      lazy-evaluation.

  Yields:
    None
  """
  # Hide the function from the traceback. Is supported by Pytest and IPython 7
  __tracebackhide__ = True  # pylint: disable=unused-variable,invalid-name

  try:
    yield
  except Exception as e:  # pylint: disable=broad-except
    reraise(e, prefix=prefix, suffix=suffix)

