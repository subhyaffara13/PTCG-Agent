import random

def parallel(request):
    """
    Fixture for parallel keyword argument for numba.jit.
    """
    return request.param


def parallel(results_: _Sequence[_ods_ir.Type], lower_bound: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], upper_bound: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], step: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], init_vals: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ParallelOp]:
  op = ParallelOp(results_=results_, lowerBound=lower_bound, upperBound=upper_bound, step=step, initVals=init_vals, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def parallel(*layers):
  """Combinator for composing layers in parallel.

  The layer resulting from this combinator is often used with the FanOut and
  FanInSum layers.

  Args:
    *layers: a sequence of layers, each an (init_fun, apply_fun) pair.

  Returns:
    A new layer, meaning an (init_fun, apply_fun) pair, representing the
    parallel composition of the given sequence of layers. In particular, the
    returned layer takes a sequence of inputs and returns a sequence of outputs
    with the same length as the argument `layers`.
  """
  nlayers = len(layers)
  init_funs, apply_funs = zip(*layers)
  def init_fun(rng, input_shape):
    rngs = random.split(rng, nlayers)
    return zip(*[init(rng, shape) for init, rng, shape
                 in zip(init_funs, rngs, input_shape)])
  def apply_fun(params, inputs, **kwargs):
    rng = kwargs.pop('rng', None)
    rngs = random.split(rng, nlayers) if rng is not None else (None,) * nlayers
    return [f(p, x, rng=r, **kwargs) for f, p, x, r in zip(apply_funs, params, inputs, rngs)]
  return init_fun, apply_fun

