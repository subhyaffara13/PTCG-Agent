
def _deserialize_specs(
    serialized_specs: jax.Array,
) -> tuple[tree_util.PyTreeDef, tuple[api.ShapeDtypeStruct, ...]]:
  """Deserializes the specs from the serialized specs.

  DO NOT USE THIS FUNCTION EXCEPT FOR THE INTERNAL IMPLEMENTATION OF
  colocated_python. See serialize() for details.
  """
  data_array = serialized_specs.addressable_shards[0].data
  data = base64.b64decode(data_array.item().encode("ascii"))
  return _deserialize(data)

