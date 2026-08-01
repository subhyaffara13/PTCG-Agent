
def _unshard_shaped_array(mesh: Mesh, check_vma, spec, aval: core.ShapedArray
                          ) -> core.ShapedArray:
  assert isinstance(aval, core.ShapedArray)
  if check_vma and spec.unreduced != aval.mat.unreduced:
    raise ValueError(
        "out_specs passed to shard_map should be equal to the unreduced"
        f" present on the out_aval. Got out_specs={spec} and"
        f" out_aval={aval.str_short(True)}")
  if check_vma and spec.reduced != aval.mat.reduced:
    raise ValueError(
        "out_specs passed to shard_map should be equal to the reduced present"
        f" on the out_aval. Got out_specs={spec} and"
        f" out_aval={aval.str_short(True)}")
  names = _spec_to_names(spec)
  new_shape = tuple(sz * prod(mesh.shape[n] for n in names.get(i, ()))
                    for i, sz in enumerate(aval.shape))
  names_spec = spec._normalized_spec_for_aval(aval.ndim).partitions
  if aval.ndim == 0:
    out_spec = P(unreduced=spec.unreduced, reduced=spec.reduced)
  else:
    out_spec = []
    for name_s, aval_s in zip(names_spec, aval.sharding.spec.partitions):
      if name_s and not aval_s:
        out_spec.append(name_s)
      elif aval_s and not name_s:
        out_spec.append(aval_s)
      elif not name_s and not aval_s:
        out_spec.append(None)
      else:
        assert name_s and aval_s
        name_s = name_s if isinstance(name_s, tuple) else (name_s,)
        aval_s = aval_s if isinstance(aval_s, tuple) else (aval_s,)
        out_spec.append(name_s + aval_s)
    out_spec = PartitionSpec(*out_spec, unreduced=spec.unreduced,
                             reduced=spec.reduced)
  new_mesh = (mesh.abstract_mesh if get_abstract_mesh().empty else
              get_abstract_mesh())
  new_sharding = NamedSharding(new_mesh, out_spec)
  manual_axes = set(new_mesh.manual_axes)
  vma = frozenset(v for v in aval.mat.varying if v in manual_axes)
  # TODO(yashkatariya): Handle partial manual unreduced/reduced.
  out_mat = core.ManualAxisType(varying=vma)
  return aval.update(shape=new_shape, sharding=new_sharding,
                     manual_axis_type=out_mat)

