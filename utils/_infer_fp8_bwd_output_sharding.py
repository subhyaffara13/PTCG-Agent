
def _infer_fp8_bwd_output_sharding(mesh, arg_shapes, layout):
  # Prepare variadic_args for the original function
  has_bias = False  # Adjust as needed
  has_dbias = False  # Adjust as needed
  variadic_args = (has_bias, has_dbias)  # Dummy value, adjust as necessary

  # Call the original function with the required parameters
  output_shardings = _infer_bwd_output_sharding(mesh, arg_shapes, layout, variadic_args)

  # Prepare amax_sharding
  amax_sharding = NamedSharding(mesh, PartitionSpec())  # Use a default spec or adjust as needed

  # Append amax_sharding for each output sharding
  out_shardings_with_amax = output_shardings + [amax_sharding] * 4

  return out_shardings_with_amax

