
def _shard_shaped_array(mesh: Mesh, manual_axes: frozenset, check_vma,
                        spec, aval: core.ShapedArray) -> core.ShapedArray:
  assert isinstance(aval, core.ShapedArray)
  if spec.unreduced != aval.sharding.spec.unreduced:
    raise ValueError(
        f"in_specs containing unreduced {spec} passed to shard_map should be"
        " equal to the unreduced present on the in_aval"
        f" {aval.str_short(True)}")
  if spec.reduced != aval.sharding.spec.reduced:
    raise ValueError(
        f"in_specs containing reduced {spec} passed to shard_map should be"
        f" equal to the reduced present on the in_aval {aval.str_short(True)}")
  names = _spec_to_names(spec)
  new_shape = tuple(sz // prod(mesh.shape[n] for n in names.get(i, ()))
                    for i, sz in enumerate(aval.shape))
  manual_mesh = _as_manual_mesh(mesh, manual_axes)
  new_sharding = aval.sharding.update(
      mesh=manual_mesh,
      spec=core.modify_spec_for_auto_manual(aval.sharding.spec, manual_mesh))
  vma = (_spec_to_vma(spec) if check_vma else frozenset()) | aval.mat.varying
  unreduced = aval.sharding.spec.unreduced if check_vma else frozenset()
  reduced = aval.sharding.spec.reduced if check_vma else frozenset()
  mat = core.ManualAxisType(varying=vma, unreduced=unreduced, reduced=reduced)
  return aval.update(shape=new_shape, sharding=new_sharding,
                     manual_axis_type=mat)

