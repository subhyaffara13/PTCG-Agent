
def unreachable(*, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> UnreachableOp:
  return UnreachableOp(loc=loc, ip=ip)


def unreachable(*args, out_avals=None, exc_type=TypeError,
                message='unreachable'):
  """Fail when evaluated concretely (but allow for staging).

  This function allows one to assert an impossibility of
  evaluation. It can be used to guarantee that evaluation does not
  "reach" a certain point in the sense that it does not execute, but
  it can nonetheless be staged out by JAX without error.

  Args:
    *args: The arbitrary pytree of arguments to the function.
    out_avals: Optional specification of the output types of this
     function invocation from the point of view of staging. If
     ``None``, these are chosen as equal to types of input arguments.
    exc_type: Optional constructor for the Python exception raised if
      evaluated.
    message: Optional string message for the Python exception raised
      if evaluated.

  """
  if out_avals is None:
    out_avals = tree_map(core.typeof, args)

  args_flat, in_tree = tree_flatten(args)
  out_avals_flat, out_tree = tree_flatten(out_avals)
  out = unreachable_p.bind(*args_flat, out_avals=out_avals_flat,
                           exc_type=exc_type, message=message)
  return tree_unflatten(out_tree, out)

