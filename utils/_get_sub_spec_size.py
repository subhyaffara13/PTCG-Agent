import math


def _get_sub_spec_size(mesh, sub_spec):
  if isinstance(sub_spec, tuple):
    return math.prod(mesh.shape[s] for s in sub_spec)
  return mesh.shape[sub_spec]

