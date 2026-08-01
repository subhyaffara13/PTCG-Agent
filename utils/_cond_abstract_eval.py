
def _cond_abstract_eval(*avals: core.AbstractValue,
                        branches: Sequence[core.ClosedJaxpr], **_):
  joined_effects = _join_cond_effects(branches)
  disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(joined_effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `cond`: {disallowed_effects}')
  b0_mat = [o.mat for o in branches[0].out_avals]
  for branch in branches[1:]:
    b_mat = [o.mat for o in branch.out_avals]
    if b0_mat != b_mat:
      raise Exception("The branches of cond produced mismatched varying manual "
                      f"axes. Got {b0_mat} and {b_mat}. Please open an issue "
                      "at https://github.com/jax-ml/jax/issues, and as a "
                      "temporary workaround pass the check_vma=False argument "
                      "to `jax.shard_map`")
  return branches[0].out_avals, joined_effects

