
def run_interceptors(
  orig_method: Callable[..., Any],
  module: 'Module',
  *args,
  **kwargs,
) -> Any:
  """Runs method interceptors."""
  method_name = _get_fn_name(orig_method)
  fun = functools.partial(orig_method, module)
  context = InterceptorContext(module, method_name, fun)

  def wrap_interceptor(interceptor, fun):
    """Wraps `fun` with `interceptor`."""

    @functools.wraps(fun)
    def wrapped(*args, **kwargs):
      return interceptor(fun, args, kwargs, context)

    return wrapped

  # Wraps interceptors around the original method. The innermost interceptor is
  # the last one added and directly wrapped around the original bound method.
  for interceptor in _global_interceptor_stack:
    fun = wrap_interceptor(interceptor, fun)
  return fun(*args, **kwargs)

