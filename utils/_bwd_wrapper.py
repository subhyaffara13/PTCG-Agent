
def _bwd_wrapper(treedef, bwd_fn, tangent):
  vars_grad, *inputs_grad = bwd_fn(tangent)
  vars_grad = treedef.unflatten(vars_grad)
  return (vars_grad, *inputs_grad)

