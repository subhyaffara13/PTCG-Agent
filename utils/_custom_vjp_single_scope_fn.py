import functools
from typing import Any, Callable

def _custom_vjp_single_scope_fn(
  fn: Callable[..., Any],
  backward_fn: Callable[..., Any],
  grad_vars: CollectionFilter = 'params',
  nondiff_argnums=(),
):
  nodiff_fn = functools.partial(fn, needs_residual=False)
  forward_fn = functools.partial(fn, needs_residual=True)
  return lift.custom_vjp(
    nodiff_fn, forward_fn, backward_fn, grad_vars, nondiff_argnums
  )

