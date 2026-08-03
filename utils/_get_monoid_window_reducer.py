from typing import Callable

def _get_monoid_window_reducer(
    monoid_op, xs: Sequence[Array]
) -> Callable | None:
  if len(xs) != 1:
    return None
  x, = xs
  aval = core.typeof(x)
  if core.is_concrete(x) and aval.shape == ():
    val = core.to_concrete_value(x)
    if monoid_op is lax.add:
      return val == 0 and _reduce_window_sum
    elif monoid_op is lax.max:
      return (val == lax._get_max_identity(aval.dtype)
              and _reduce_window_max)
    elif monoid_op is lax.min:
      return (val == lax._get_min_identity(aval.dtype)
              and _reduce_window_min)
  return None

