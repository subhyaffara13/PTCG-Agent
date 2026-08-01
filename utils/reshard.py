
def reshard(input: _ods_ir.Value, sharding: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ReshardOp(input=input, sharding=sharding, results=results, loc=loc, ip=ip).result


def reshard(xs, out_shardings):
  x_flat, treedef = tree_flatten(xs)
  shardings_flat = flatten_axis_resources(
      "reshard out_shardings", treedef, out_shardings, tupled_args=True)
  x_avals_flat = [core.shaped_abstractify(x) for x in x_flat]
  out_flat = []
  for x, x_aval, s in safe_zip(x_flat, x_avals_flat, shardings_flat):
    ds = canonicalize_sharding(s, 'reshard', check_mesh_consistency=False)
    if ds is None:
      raise ValueError(
          'Reshard should only be used with out_shardings which are non-None '
          f'and have a non-empty mesh. Got sharding {s}.'
      )
    ds = ds.update(spec=ds.spec._normalized_spec_for_aval(x_aval.ndim))
    cmesh = (s.mesh if (isinstance(s, NamedSharding) and
                        isinstance(s.mesh, mesh_lib.Mesh))
             else None)
    out_flat.append(reshard_p.bind(x, dst_sharding=ds, concrete_mesh=cmesh))
  return tree_unflatten(treedef, out_flat)

