
def _bwd_shardy_rule(num_args, has_dbias, is_fp8):
  input_sharding = tuple(ArrayMapping(f'{BATCHING}{n}') for n in range(num_args))

  if has_dbias:
    output_sharding = input_sharding[0:4]
  else:
    output_sharding = input_sharding[0:3]
  if is_fp8:
    amax = ArrayMapping(f'{BATCHING}{num_args}')
    output_sharding += (amax, amax, amax, amax)
  return SdyShardingRule(input_sharding, output_sharding)

