
def _flatten_with_path(dcls):
  path = []
  keys = []
  for k, v in sorted(dcls.__dict__.items()):
    keys.append(k)  # generate same aux data as flatten without path
    k = jax.tree_util.GetAttrKey(k)
    path.append((k, v))
  return path, tuple(keys)

