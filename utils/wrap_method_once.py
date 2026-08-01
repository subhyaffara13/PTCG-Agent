
def wrap_method_once(fun: Callable[..., Any]) -> Callable[..., Any]:
  """Manages Module state for a given user-defined method.

  Args:
    fun: User-defined Module method to manage state for.

  Returns:
    Wrapped method.
  """
  # Don't rewrap methods that have already had the state management wrapper
  # applied in the decorator stack.  This wrapper should always be applied
  # before transformation wrappers.
  if hasattr(fun, 'method_handler_wrapped'):
    return fun

  @functools.wraps(fun)
  def wrapped_module_method(*args, **kwargs):
    # We might have incorrectly wrappped a callable
    # that is not a method. Check whether the first arg is self,
    # otherwise call the wrapped function as is.
    if args and isinstance(args[0], Module):
      self, args = args[0], args[1:]
      return self._call_wrapped_method(fun, args, kwargs)
    else:
      return fun(*args, **kwargs)

  wrapped_module_method.method_handler_wrapped = True  # type: ignore[attr-defined]
  return wrapped_module_method

