
def annotate_function(func: Callable, name: str | None = None,
                      **decorator_kwargs):
  """Decorator that generates a trace event for the execution of a function.

  For example:

  >>> @jax.profiler.annotate_function
  ... def f(x):
  ...   return jnp.dot(x, x.T).block_until_ready()
  >>>
  >>> result = f(jnp.ones((1000, 1000)))

  This will cause an "f" event to show up on the trace timeline if the
  function execution occurs while the process is being traced by TensorBoard.

  Arguments can be passed to the decorator via :py:func:`functools.partial`.

  >>> from functools import partial

  >>> @partial(jax.profiler.annotate_function, name="event_name")
  ... def f(x):
  ...   return jnp.dot(x, x.T).block_until_ready()

  >>> result = f(jnp.ones((1000, 1000)))
  """

  name = name or getattr(func, '__qualname__', None)
  name = name or func.__name__
  @wraps(func)
  def wrapper(*args, **kwargs):
    with TraceAnnotation(name, **decorator_kwargs):
      return func(*args, **kwargs)
  return wrapper

