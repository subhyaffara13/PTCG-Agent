
def _generic_effectful_abstract_eval(abstract_eval, prim):
  def abstract_eval_(*args, **kwargs):
    return abstract_eval(*args, **kwargs), {GenericEffect(prim)}
  return abstract_eval_

