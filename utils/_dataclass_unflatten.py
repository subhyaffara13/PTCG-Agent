
def _dataclass_unflatten(dcls, keys, values):
  """Creates a chex dataclass from a flatten jax.tree_util representation."""
  dcls_object = dcls.__new__(dcls)
  attribute_dict = dict(zip(keys, values))
  # Looping over fields instead of keys & values preserves the field order.
  # Using dataclasses.fields fails because dataclass uids change after
  # serialisation (eg, with cloudpickle).
  for field in dcls.__dataclass_fields__.values():
    if field.name in attribute_dict:  # Filter pseudo-fields.
      object.__setattr__(dcls_object, field.name, attribute_dict[field.name])
  # Need to manual call post_init here as we have avoided calling __init__
  if getattr(dcls_object, "__post_init__", None):
    dcls_object.__post_init__()
  return dcls_object

