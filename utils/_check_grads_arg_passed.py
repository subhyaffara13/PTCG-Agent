import functools

def _check_grads_arg_passed(f: F) -> F:
  @functools.wraps(f)
  def _check_grads_wrapper(self, model, grads=MISSING, **kwargs):
    if isinstance(grads, _Missing):
      raise TypeError(
        'Missing required argument `grads`. As of Flax 0.11.0 update requires both (model, grads) arguments '
        'to be passed. If you want to keep the previous use nnx.ModelAndOptimizer instead of nnx.Optimizer.'
      )
    return f(self, model, grads, **kwargs)
  return _check_grads_wrapper # type: ignore

