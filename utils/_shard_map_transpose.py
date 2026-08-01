
def _shard_map_transpose(out_cts, *args, jaxpr: core.Jaxpr, mesh, in_specs,
                         out_specs, check_vma, newly_manual_axes):
  mb_div = lambda x, y: x / y if y != 1 else x
  out_cts = [
      ad.Zero(shard_aval(mesh, newly_manual_axes, check_vma, sp.to_ct_spec(), x.aval))
      if type(x) is ad.Zero else x if check_vma or dtypes.dtype(x) == dtypes.float0
      else mb_div(x, prod(map(mesh.shape.get, _unmentioned2(mesh, sp.to_ct_spec(), newly_manual_axes))))
      for sp, x in zip(out_specs, out_cts)
  ]
  args = [x if type(x) is not ad.UndefinedPrimal else
          ad.UndefinedPrimal(shard_aval(mesh, newly_manual_axes, check_vma, sp.to_ct_spec(), x.aval))
          for sp, x in zip(in_specs, args)]
  all_args, in_tree = tree_flatten((out_cts, tuple(args)))

  def fun_trans_callable(*right_flat):
    right_cts, primals_or_undefs = tree_unflatten(in_tree, right_flat)
    left_cts = ad.backward_pass(jaxpr, False, (), primals_or_undefs, right_cts)
    left_cts = [x if type(x) is ad.Zero or check_vma
                else lax_parallel.psum(x, tuple(_unmentioned2(mesh, sp.to_ct_spec(), newly_manual_axes)))
                for sp, x in zip(in_specs, left_cts)]
    left_specs_nz = tuple(
        s.to_ct_spec() for ct, s in zip(left_cts, in_specs)
        if ct is not None and type(ct) is not ad.Zero)
    return FlatTree.flatten(left_cts).with_aux(left_specs_nz)

  dbg = jaxpr.debug_info.with_unknown_names()
  new_in_specs = (
      [s.to_ct_spec() for s, x in zip(out_specs, out_cts) if type(x) is not ad.Zero] +
      [s for s, x in zip(in_specs, args) if type(x) is not ad.UndefinedPrimal])

  left_ct = shard_map_p.bind(
      *all_args, subfuns=(fun_trans_callable,), mesh=mesh, in_specs=tuple(new_in_specs),
      check_vma=check_vma, newly_manual_axes=newly_manual_axes, debug_info=dbg)
  left_cts = left_ct.unflatten()
  return [ad.Zero(unshard_aval(mesh, check_vma, sp.to_ct_spec(), x.aval))
          if type(x) is ad.Zero else x for sp, x in zip(in_specs, left_cts)]

