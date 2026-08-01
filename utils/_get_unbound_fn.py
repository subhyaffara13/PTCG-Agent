
def _get_unbound_fn(method_or_fn: Callable[..., Any]) -> Callable[..., Any]:
  """Returns an unbound function from a method that is possibly bound.

  This means that if the passed function belongs of an instance of a class, then
  the returned function does no longer depend on the instance, which is passed
  as the first argument to the function.

  Args:
    method_or_fn: A class method or function.

  Returns:
    An unbound version of input function.
  """
  if inspect.ismethod(method_or_fn) and isinstance(
    method_or_fn.__self__, Module
  ):  # pytype: disable=attribute-error
    method_or_fn = method_or_fn.__func__  # pytype: disable=attribute-error

  # The method should be callable, and it should have at least one argument
  # representing the class that is passed in.
  if (
    not callable(method_or_fn)
    or len(inspect.signature(method_or_fn).parameters) < 1
  ):
    raise errors.ApplyModuleInvalidMethodError(method_or_fn)

  return method_or_fn


def _get_unbound_fn(method_or_fn: tp.Callable) -> tp.Callable:
  if inspect.ismethod(method_or_fn) and isinstance(
    method_or_fn.__self__, Module
  ):  # pytype: disable=attribute-error
    method_or_fn = method_or_fn.__func__  # pytype: disable=attribute-error
  if (
    not callable(method_or_fn)
    or len(inspect.signature(method_or_fn).parameters) < 1
  ):
    raise errors.ApplyModuleInvalidMethodError(method_or_fn)

  return method_or_fn

