import functools
from typing import Any, Callable, Optional

def warn_deprecated_function(
    fun: Callable[..., Any],
    replacement: Optional[str] = None,
    version_removed: Optional[str] = None,
) -> Callable[..., Any]:
  """A decorator to mark a function definition as deprecated.

  Args:
    fun: the deprecated function.
    replacement: name of the function to be used instead.
    version_removed: version of optax in which the function was/will be removed.

  Returns:
    The wrapped function.

  Example usage:
  >>> @functools.partial(warn_deprecated_function, replacement='g')
  ... def f(a, b):
  ...   return a + b
  """
  if hasattr(fun, '__name__'):
    warning_message = f'The function {fun.__name__} is deprecated.'
  else:
    warning_message = 'The function is deprecated.'
  if replacement:
    warning_message += f' Please use {replacement} instead.'
  if version_removed:
    warning_message += (
        f' This function will be/was removed in optax {version_removed}.'
    )

  @functools.wraps(fun)
  def new_fun(*args, **kwargs):
    warnings.warn(warning_message, category=DeprecationWarning, stacklevel=2)
    return fun(*args, **kwargs)

  return new_fun


def warn_deprecated_function(
    fun: Callable[..., Any], replacement: Optional[str] = None
) -> Callable[..., Any]:
  """A decorator to mark a function definition as deprecated.

  Example usage:
  >>> @functools.partial(chex.warn_deprecated_function, replacement='g')
  ... def f(a, b):
  ...   return a + b

  Args:
    fun: the deprecated function.
    replacement: name of the function to be used instead.

  Returns:
    the wrapped function.
  """
  if hasattr(fun, '__name__'):
    warning_message = f'The function {fun.__name__} is deprecated.'
  else:
    warning_message = 'The function is deprecated.'
  if replacement:
    warning_message += f' Please use {replacement} instead.'

  @functools.wraps(fun)
  def new_fun(*args, **kwargs):
    warnings.warn(warning_message, category=DeprecationWarning, stacklevel=2)
    return fun(*args, **kwargs)

  return new_fun

