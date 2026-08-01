
def broadcasting_sharding_rule(name, *avals, **kwargs):
  if not isinstance(name, str):
    raise RuntimeError(
      "First argument of broadcasting_sharding_rule should be a name."
      f" Got {name}")
  mesh = None
  for a in avals:
    if a.sharding is not None and not a.sharding.mesh.empty:
      if mesh is not None and mesh != a.sharding.mesh:
        raise core.ShardingTypeError(
            f'Mesh for all inputs should be equal. Got one mesh: {mesh} and'
            f' another mesh: {a.sharding.mesh}')
      mesh = a.sharding.mesh
  mesh = get_abstract_mesh() if mesh is None else mesh

  shapes = [aval.shape for aval in avals if aval.shape]
  if not shapes:
    return NamedSharding(mesh, P())
  if len({len(shape) for shape in shapes}) != 1:
    msg = '{}: arrays must have same number of dimensions, got {}.'
    raise TypeError(msg.format(name, ', '.join(map(str, map(tuple, shapes)))))

  specs = [a.sharding.spec.partitions for a in avals if a.shape]

  result_specs = [None] * len(shapes[0])
  for i, (ss, ds) in enumerate(zip(zip(*specs), zip(*shapes))):
    if all(ss[0] == s for s in ss[1:]):
      # if all dimension shardings are same, the resulting dimension sharding is
      # the same.
      result_specs[i] = ss[0]
    else:
      non_trivial_s = [s for s, d in zip(ss, ds)
                       if not (core.definitely_equal(d, 1) and s is None)]
      if not non_trivial_s:
        result_specs[i] = None
      elif all(non_trivial_s[0] == s for s in non_trivial_s[1:]):
        result_specs[i] = non_trivial_s[0]
      else:
        for s in ss:
          if result_specs[i] is None and s is not None:
            result_specs[i] = s
          elif (result_specs[i] is not None and s is not None and
                result_specs[i] != s):
            raise core.ShardingTypeError(
                f'{name} got incompatible shardings for broadcasting: '
                f'{", ".join(map(str, map(tuple, specs)))}.')
  return NamedSharding(mesh, P(*result_specs))

