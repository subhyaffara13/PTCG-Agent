
def instantiate_zeros(tangent):
  if type(tangent) is Zero:
    if hasattr(tangent.aval, 'sharding'):
      # TODO(dougalm, yashkatariya): Delete this context manager once we figure
      # out how to ensure jaxpr arguments always have the context mesh.
      with mesh_lib.use_abstract_mesh(tangent.aval.sharding.mesh):
        return zeros_like_aval(tangent.aval)
    return zeros_like_aval(tangent.aval)
  return tangent

