from typing import Callable

def when(
    condition: bool | jax_typing.ArrayLike, /
) -> Callable[[Callable[[], None]], None]:
  """Calls the decorated function when the condition is met.

  Args:
    condition: If a boolean, this is equivalent to ``if condition: f()``. If an
      array, ``when`` produces a :func:`jax.lax.cond` with the decorated
      function as the true branch.

  Returns:
    A decorator.
  """
  def _wrapped(f):
    if isinstance(condition, bool):
      if condition:
        f()
    else:
      conditionals.cond(condition, f, lambda: None)
  return _wrapped


def when(cond):
  with ir.InsertionPoint(scf.IfOp(cond).then_block):
    yield
    scf.yield_([])

