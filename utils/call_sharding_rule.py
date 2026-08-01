
def call_sharding_rule(prim, sh_rule, ur_rule, num_out, *avals, **kwargs):
  cur_mesh = mesh_lib.get_abstract_mesh()
  aval_mesh = _get_abstract_mesh_from_avals(avals)
  if ((cur_mesh.empty or cur_mesh._are_all_axes_auto_or_manual) and
      (aval_mesh.empty or aval_mesh._are_all_axes_auto_or_manual)):
    aval_mesh = cur_mesh if aval_mesh.empty else aval_mesh
    out_s = NamedSharding(aval_mesh, P())
    return out_s if num_out is None else [out_s] * num_out
  if sh_rule is None:
    raise core.ShardingTypeError(
        f'sharding rule for {prim.name} is not implemented. Please file an'
        ' issue at https://github.com/jax-ml/jax/issues. You can work around'
        ' this error by dropping that operation into full auto sharding'
        ' mode via: `jax.sharding.auto_axes(fun, out_shardings=...)`')
  out_s = sh_rule(*avals, **kwargs)
  unreduced, reduced = call_ur_rule(prim, ur_rule, out_s, num_out, *avals,
                                    **kwargs)
  up = lambda sh, u, r: sh.update(spec=sh.spec.update(unreduced=u, reduced=r))
  return (up(out_s, unreduced, reduced) if num_out is None else
          [up(s, u, r) for s, u, r in zip(out_s, unreduced, reduced)])

