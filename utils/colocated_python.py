from typing import Any, Callable

def colocated_python(fun: Callable[..., Any]):
  """Executes the given Python function on the same devices as the arguments.

  The returned colocated Python callable lets the user run a serializable Python
  function on the same devices as the arguments, potentially on remote hosts.

  Python callable implements `specialize` and `__call__` methods. See their
  docstrings for details and https://docs.jax.dev/en/latest/notebooks/colocated-python.html
  for examples.

  Args:
    fun: An original function to wrap as an I/O callable.

  Returns:
    Colocated Python callable with no initial specialization.
  """
  return make_callable(
      fun, api_util.fun_sourceinfo(fun), api_util.fun_signature(fun)
  )

