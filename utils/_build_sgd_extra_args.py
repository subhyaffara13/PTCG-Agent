
def _build_sgd_extra_args():

  def init_fn(params):
    del params
    return {'foo': 1}

  def update_fn(grads, state, params=None, *, foo=None, **extra_args):
    del extra_args, foo, params
    return grads, state

  t = base.GradientTransformationExtraArgs(init_fn, update_fn)
  return combine.chain(_build_sgd(), t)


def _build_sgd_extra_args():

  def init_fn(params):
    del params
    return {'foo': 1}

  def update_fn(grads, state, params=None, *, foo=None, **extra_args):
    del extra_args, foo, params
    return grads, state

  t = base.GradientTransformationExtraArgs(init_fn, update_fn)
  return combine.chain(_build_sgd(), t)

