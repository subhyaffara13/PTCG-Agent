
def _infer_fp8_fwd_output_sharding(mesh, arg_shapes, is_training, layout):
  # Prepare variadic_args for the original function
  has_bias = False  # Adjust as needed
  variadic_args = (has_bias, None)  # Dummy value, adjust as necessary

  # Call the original function with the required parameters
  output_sharding = _infer_fwd_output_sharding(mesh, arg_shapes, variadic_args, is_training, layout)
  amax_sharding = NamedSharding(mesh, PartitionSpec())
  if is_training:
    out_sharding, activation_sharding = output_sharding[0], output_sharding[1]
    return [out_sharding, amax_sharding, amax_sharding, activation_sharding]
  return output_sharding + [amax_sharding, amax_sharding]

