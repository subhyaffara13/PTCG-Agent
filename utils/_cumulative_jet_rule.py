from typing import Callable

def _cumulative_jet_rule(primals_in, series_in, *, axis: int, reverse: bool,
                         combine_fn: Callable):
  # Irrespective of backend, we always use the parallel prefix scan
  # implementation when differentiating because reduce_window is not
  # arbitrarily differentiable.
  return jet2(partial(lax.associative_scan, combine_fn, axis=axis,
                     reverse=reverse),
             primals_in, series_in)

