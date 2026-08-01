
def create_deprecated_function_alias(fun, new_name, deprecated_alias):
  """Create a deprecated alias for a function.

  Example usage:
  >>> g = create_deprecated_function_alias(f, 'path.f', 'path.g')

  Args:
    fun: the deprecated function.
    new_name: the new name to use (you may include the path for clarity).
    deprecated_alias: the old name (you may include the path for clarity).

  Returns:
    the wrapped function.
  """

  @functools.wraps(fun)
  def new_fun(*args, **kwargs):
    warnings.warn(
        f'The function {deprecated_alias} is deprecated, '
        f'please use {new_name} instead.',
        category=DeprecationWarning,
        stacklevel=2)
    return fun(*args, **kwargs)
  return new_fun

