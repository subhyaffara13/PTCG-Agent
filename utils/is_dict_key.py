
def is_dict_key(key) -> bool:
  return isinstance(key, (jax.tree_util.DictKey, jax.tree_util.GetAttrKey))

