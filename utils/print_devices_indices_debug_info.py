
def print_devices_indices_debug_info(
    restore_args: PyTree,
):
  """Prints debug info before restoring the parameter."""
  arrays = jax.tree.map(abstract_arrays.to_shape_dtype_struct, restore_args)
  param_names = tree_utils.get_param_names(arrays, include_empty_nodes=False)
  flat_arrays, _ = jax.tree.flatten(arrays)
  flat_param_names, _ = jax.tree.flatten(param_names)
  assert len(flat_arrays) == len(flat_param_names)

  for arr, param_name in zip(flat_arrays, flat_param_names):
    devices_indices_map = arr.sharding.devices_indices_map(arr.shape)
    logging.vlog(1, 'Device -> index map for %s.', param_name)
    for d, idx in devices_indices_map.items():
      logging.vlog(1, '  %s -> %s', d, idx)

