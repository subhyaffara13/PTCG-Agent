
def get_replicated_axes(spec, mesh):
  flat_spec = frozenset(
      s for s in flatten_spec(spec)
      if s is not None and s is not PartitionSpec.UNCONSTRAINED)
  return frozenset(mesh.axis_names) - (flat_spec | spec.unreduced | spec.reduced)

