
def _serialize_specs(
    specs_treedef: tree_util.PyTreeDef,
    specs_leaves: tuple[api.ShapeDtypeStruct, ...],
    devices: DeviceList,
) -> jax.Array:
  """Serializes the output specs into a jax.Array of string type.

  DO NOT USE THIS FUNCTION EXCEPT FOR THE INTERNAL IMPLEMENTATION OF
  colocated_python. See serialize() for details.
  """
  if not hasattr(np.dtypes, "StringDType"):
    raise TypeError(
        "Serializing Colocated Python requires StringDType. Please use"
        " numpy to 2.0.0 or later, or explicitly provide an output spec"
        " function."
    )

  s_bytes = _serialize((specs_treedef, specs_leaves))
  s_str = base64.b64encode(s_bytes).decode("ascii")
  s_np_array = np.array(s_str, dtype=np.dtypes.StringDType())

  # TODO(jmudigonda): Revisit this when JAX supports HLO sharding for making
  # jax.Array via make_array_from_single_device_arrays. We should then use a
  # sharding that spans all the execution devices - not just the addressable
  # ones.
  addressable_devices = devices.addressable_device_list
  mesh = jax.sharding.Mesh(tuple(addressable_devices), ("x",))
  replicated_sharding = jax.sharding.NamedSharding(
      mesh, jax.sharding.PartitionSpec()
  )

  out_arrays = [
      jax.device_put(s_np_array, device) for device in addressable_devices
  ]
  return jax.make_array_from_single_device_arrays(
      arrays=out_arrays,
      sharding=replicated_sharding,
      shape=(),
  )

