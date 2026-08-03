from typing import Callable

def _cumulative_jvp_rule(primals, tangents, *, axis: int, reverse: bool,
                         combine_fn: Callable):
  # Irrespective of backend, we always use the parallel prefix scan
  # implementation when differentiating because reduce_window is not
  # arbitrarily differentiable.
  return api.jvp(partial(associative_scan, combine_fn, axis=axis,
                         reverse=reverse),
                 primals, tangents)

