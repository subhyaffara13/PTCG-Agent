
def _cond_typecheck(bind_time, *in_atoms, branches, **params):
  del params
  if not bind_time:
    _, *in_atoms = in_atoms
  avals = [x.aval for x in in_atoms]
  tc = partial(_typecheck_param, 'cond')
  tc(branches, 'branches', 'tuple of ClosedJaxpr',
     type(branches) is tuple and
     all(type(x) is core.ClosedJaxpr for x in branches))

  if len(branches) == 0:
    raise core.JaxprTypeError('cond requires at least one branch function')

  jaxpr0 = branches[0]
  jaxpr0_in_avals_str = _avals_short(jaxpr0.in_avals)
  jaxpr0_out_avals_str = _avals_short(jaxpr0.out_avals)
  joined_effects = _join_cond_effects(branches)
  disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(joined_effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `cond`: {disallowed_effects}')

  for i, jaxpr in enumerate(branches[1:]):
    if len(jaxpr0.in_avals) != len(jaxpr.in_avals):
      raise core.JaxprTypeError(
        f'cond branch 0 takes {len(jaxpr0.in_avals)} inputs, '
        f'branch {i+1} takes {len(jaxpr.in_avals)}')
    if len(jaxpr0.out_avals) != len(jaxpr.out_avals):
      raise core.JaxprTypeError(
        f'cond branch 0 outputs {len(jaxpr0.out_avals)} values, '
        f'branch {i+1} outputs {len(jaxpr.out_avals)}')
    if not all(map(core.typematch, jaxpr0.in_avals, jaxpr.in_avals)):
      raise core.JaxprTypeError(
        f'cond branches 0 and {i+1} have mismatching input types: '
        f'{jaxpr0_in_avals_str} vs {_avals_short(jaxpr.in_avals)}')
    if not all(map(core.typematch, jaxpr0.out_avals, jaxpr.out_avals)):
      raise core.JaxprTypeError(
        f'cond branches 0 and {i+1} have mismatching output types: '
        f'{jaxpr0_out_avals_str} vs {_avals_short(jaxpr.out_avals)}')

  if len(avals) != 1 + len(jaxpr0.in_avals):
    raise core.JaxprTypeError(
      f'cond called with {len(avals) - 1} non-predicate operands, '
      f'but branches take {len(jaxpr0.in_avals)} inputs')

  index_aval, *op_avals = avals
  if index_aval.dtype != np.int32:
    raise core.JaxprTypeError(
      f'cond called with index of type {index_aval.dtype} instead of int32')
  if not all(map(core.typecompat, jaxpr0.in_avals, op_avals)):
    raise core.JaxprTypeError(
      f'cond branches take input types {jaxpr0_in_avals_str}, '
      f'called with operands of type {_avals_short(op_avals)}')
  return jaxpr0.out_avals, joined_effects

