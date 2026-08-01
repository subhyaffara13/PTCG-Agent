
def _linear_solve_abstract_eval(*args, const_lengths, jaxprs):
  args_to_raise = args[sum(const_lengths):]
  # raise aux_args to shaped arrays as well if present
  # number of aux args is the difference in out_avals
  # of solve and matvec (since they map to the same vector space)
  num_aux = len(jaxprs.solve.out_avals) - len(jaxprs.matvec.out_avals)
  if num_aux > 0:
    args_to_raise += tuple(jaxprs.solve.out_avals[-num_aux:])
  out_vma = core.standard_vma_rule('linear_solve', *args_to_raise)
  if any(core.getu(a) or core.getr(a) for a in args_to_raise):
    raise NotImplementedError
  return (tuple(a.update(manual_axis_type=a.mat.update(varying=out_vma))
                for a in args_to_raise),
          jaxprs.solve.effects)

