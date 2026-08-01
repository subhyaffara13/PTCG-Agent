
def replicated_axes(aval, mesh):
  spec = aval.sharding.spec
  flat_spec = frozenset(s for s in flatten_spec(spec) if s is not None)
  return frozenset(mesh.axis_names) - (
      flat_spec | spec.unreduced | spec.reduced | aval.mat.varying |
      aval.mat.unreduced | aval.mat.reduced)

