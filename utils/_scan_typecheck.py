
def _scan_typecheck(bind_time, *in_atoms, reverse, length, num_consts,
                    num_carry, jaxpr, unroll):
  if not bind_time:
    _, *in_atoms = in_atoms
  avals = [x.aval for x in in_atoms]
  tc = partial(_typecheck_param, 'scan')
  tc(reverse, 'reverse', 'bool', type(reverse) is bool)
  tc(num_consts, 'num_consts', 'non-negative int',
     type(num_consts) is int and num_consts >= 0)
  tc(num_carry, 'num_carry', 'non-negative int',
     type(num_carry) is int and num_carry >= 0)
  tc(jaxpr, 'jaxpr', 'ClosedJaxpr', type(jaxpr) is ClosedJaxpr)
  tc(unroll, 'unroll', 'non-negative int', type(unroll) is int and unroll >= 0)

  tc(length, 'length', 'non-negative int', length >= 0)

  const_avals, init_avals, x_avals = split_list(avals, [num_consts, num_carry])
  const_avals_jaxpr, init_avals_jaxpr, x_avals_jaxpr = split_list(
      jaxpr.in_avals, [num_consts, num_carry])
  carry_avals_jaxpr, y_avals_mapped = split_list(jaxpr.out_avals, [num_carry])
  x_avals_mapped = _map(partial(core.mapped_leading_aval, length), x_avals)
  y_avals = [core.unmapped_leading_aval(length, a) for a in y_avals_mapped]

  if not all(_map(core.typematch, init_avals_jaxpr, carry_avals_jaxpr)):
    raise core.JaxprTypeError(
      f'scan input carry input and output types mismatch: '
      f'\n{_avals_short(init_avals_jaxpr)}\nvs\n{_avals_short(carry_avals_jaxpr)}')
  if not all(_map(core.typecompat, const_avals_jaxpr, const_avals)):
    raise core.JaxprTypeError(
      f'scan jaxpr takes input const types\n{_avals_short(const_avals_jaxpr)},\n'
      f'called with consts of type\n{_avals_short(const_avals)}')
  if not all(_map(core.typecompat, init_avals_jaxpr, init_avals)):
    raise core.JaxprTypeError(
      f'scan jaxpr takes input carry types\n{_avals_short(init_avals_jaxpr)},\n'
      f'called with initial carry of type\n{_avals_short(init_avals)}')
  if not all(_map(core.typecompat, x_avals_jaxpr, x_avals_mapped)):
    raise core.JaxprTypeError(
      f'scan jaxpr takes input sequence types\n{_avals_short(x_avals_jaxpr)},\n'
      f'called with sequence whose items have type\n{_avals_short(x_avals_mapped)}')
  return [*init_avals, *y_avals], core.positional_effects(jaxpr)

