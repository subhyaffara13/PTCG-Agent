
def check_shardings_are_auto(s: Sharding) -> None:
  if not isinstance(s, NamedSharding):
    return
  mesh = s.mesh.abstract_mesh
  if not all(mesh._name_to_type[i] == mesh_lib.AxisType.Auto
              for axes in s.spec
              if axes is not PartitionSpec.UNCONSTRAINED and axes is not None
              for i in (axes if isinstance(axes, tuple) else (axes,))):
    raise ValueError(
        'The spec of NamedSharding passed to with_sharding_constraint can'
        f' only refer to Auto axes of the mesh. Got spec={s.spec} and'
        f' mesh={mesh}. You probably meant to use `reshard` API?')

