
def manual_proto(
    aval: core.ShapedArray,
    manual_axes_set: frozenset[sharding_impls.MeshAxisName], mesh: Mesh):
  """Create an OpSharding proto that declares all mesh axes from `axes` as manual
  and all others as replicated.
  """
  named_mesh_shape = mesh.shape
  mesh_shape = list(named_mesh_shape.values())
  axis_order = {axis: i for i, axis in enumerate(mesh.axis_names)}

  manual_axes = sorted(manual_axes_set, key=str)
  replicated_axes = [axis for axis in mesh.axis_names
                     if axis not in manual_axes_set]

  tad_perm = ([axis_order[a] for a in replicated_axes] +
              [axis_order[a] for a in manual_axes])
  tad_shape = [1] * aval.ndim
  tad_shape.append(math.prod([named_mesh_shape[a] for a in replicated_axes]))
  tad_shape.append(math.prod([named_mesh_shape[a] for a in manual_axes]))

  proto = xc.OpSharding()
  proto.type = xc.OpSharding.Type.OTHER
  proto.tile_assignment_dimensions = tad_shape
  proto.iota_reshape_dims = mesh_shape
  proto.iota_transpose_perm = tad_perm
  proto.last_tile_dims = [xc.OpSharding.Type.REPLICATED, xc.OpSharding.Type.MANUAL]
  return proto

