import functools

def _check_wrt_arg_passed(f: F) -> F:
  @functools.wraps(f)
  def _check_wrt_wrapper(*args, wrt=MISSING, **kwargs):
    if isinstance(wrt, _Missing):
      raise TypeError(
        'Missing required argument `wrt`. As of Flax 0.11.0 the `wrt` argument is required, '
        'if you want to keep the previous use nnx.ModelAndOptimizer instead of nnx.Optimizer.'
      )
    return f(*args, wrt=wrt, **kwargs)
  return _check_wrt_wrapper  # type: ignore

