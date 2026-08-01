
def _scan_abstract_eval(*args, reverse, length, num_consts, num_carry, jaxpr,
                        unroll):
  if len(args) != len(jaxpr.in_avals):
    raise ValueError("scan number of arguments doesn't match the number "
                     "of jaxpr arguments: {len(args)} vs {len(jaxpr.in_avals)}")
  out_carry_avals, y_avals = split_list(jaxpr.out_avals, [num_carry])
  _, in_carry_avals, _ = split_list(args, [num_consts, num_carry])
  if [i.mat for i in in_carry_avals] != [o.mat for o in out_carry_avals]:
    raise ValueError(
        'Scan carry input and output got mismatched varying manual axes '
        f'{in_carry_avals} and {out_carry_avals}. Please open an '
        'issue at https://github.com/jax-ml/jax/issues, and as a '
        'temporary workaround pass the check_vma=False argument to '
        '`jax.shard_map`')
  ys_avals = _map(partial(core.unmapped_leading_aval, length), y_avals)
  return out_carry_avals + ys_avals, core.positional_effects(jaxpr)

