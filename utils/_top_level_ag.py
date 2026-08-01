
def _top_level_ag(x, aval, out_sh_, multi_dim):
  assert aval.sharding.mesh.are_all_axes_explicit, aval.sharding.mesh
  out_sh = canonicalize_sharding(out_sh_, "top_level_all_gather")
  if out_sh is None:
    raise ValueError(
        f'out_sharding passed to top_level_all_gather cannot be {out_sh_}. It'
        ' should be a PartitionSpec or NamedSharding.')
  if aval.sharding.mesh != out_sh.mesh:
    raise ValueError(
        f'Input sharding mesh {aval.sharding.mesh} should be equal to'
        f' out_sharding mesh {out_sh.mesh}')

  in_spec = aval.sharding.spec
  out_spec = out_sh.spec._normalized_spec_for_aval(len(in_spec))
  if config.remove_size_one_mesh_axis_from_type.value:
    out_spec = remove_size_one_mesh_axis(out_spec, out_sh.mesh)

  def f_shmap(x):
    # Maybe this can just be 1 AG where we gather in a new dim and then do
    # AG(new_dim) -> reshape -> transpose -> reshape but it might be expensive.
    count = 0
    for axis, (i, o) in enumerate(zip(in_spec.partitions, out_spec.partitions)):
      if i == o:
        continue
      if not multi_dim and count > 0:
        raise ValueError(
            "multiple dimensions cannot be all_gathered since multi_dim=False"
            f" passed to `top_level_all_gather`. Got {in_spec=} and {out_spec=}")
      count += 1
      if i is None:
        raise ValueError(
            f"top_level_all_gather doesn't allow input {aval} to be unsharded"
            f" on dimension {axis} when {out_spec=}.")
      i = i if isinstance(i, tuple) else (i,)
      o = o if o is None or isinstance(o, tuple) else (o,)
      if o is not None and i[:len(o)] != o:
        raise ValueError(
            'top_level_all_gather maintains `top_level_all_gather(x, ...) == x`'
            f" property. The {in_spec=} and {out_spec=} don't satisfy this"
            f' property. Please change your out_spec of array dimension {axis} so'
            " that it's a prefix of in_spec")
      axis_name = i if o is None else i[-len(o):]
      x = lax_parallel.all_gather(x, axis_name=axis_name, axis=axis,
                                  tiled=True, to='reduced')
    return x
  return api.jit(shard_map(f_shmap, out_specs=out_spec))(x)

