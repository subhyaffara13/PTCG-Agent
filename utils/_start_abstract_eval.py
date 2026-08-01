
def _start_abstract_eval(q):
  def f(*args, **kwargs):
    aval, effs = q.abstract_eval(*args, **kwargs)
    return core.AbstractFuture(aval), effs
  return f

