
def get_mat(n):
    data = np.arange(n)
    data = np.add.outer(data, data)
    return data


def get_mat(n):
    data = arange(n)
    data = add.outer(data, data)
    return data


def get_mat(mat, mesh):
  if mesh.empty:
    assert mat.empty, mat
    return mat

  axis_env = get_axis_env()
  in_axis_env = lambda i: axis_env.axis_exists(i) and i not in mesh._name_to_type
  for i in it.chain(mat.varying, mat.unreduced, mat.reduced):
    if in_axis_env(i):
      continue
    if mesh._name_to_type[i] != AxisType.Manual:
      raise ValueError(
          "Axes mentioned in `manual_axis_type` field of ShapedArray should be"
          f" of type `Manual`. Got manual_axis_type={mat} with axis: {i} of"
          f" type {mesh._name_to_type[i]}")
  if config.remove_size_one_mesh_axis_from_type.value:
    varying = frozenset(i for i in mat.varying
                        if in_axis_env(i) or mesh.shape[i] != 1)
    unreduced = frozenset(u for u in mat.unreduced if mesh.shape[u] != 1)
    reduced = frozenset(r for r in mat.reduced if mesh.shape[r] != 1)
    return mat.update(varying=varying, unreduced=unreduced, reduced=reduced)
  return mat

