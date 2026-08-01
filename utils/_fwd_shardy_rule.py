
def _fwd_shardy_rule(value_types, result_types, layout, is_training, is_fp8):
  num_args = len(value_types)
  # We only need the query and value sharding, so use placeholders for the remaining args.
  input_sharding = [ArrayMapping(f'{BATCHING}{n}') for n in range(num_args)]
  if layout == AttentionLayout.BNTH.value:
    input_sharding[0] = ArrayMapping('batch', 'nhead', 'qseq', 'head')
  else:
    input_sharding[0] = ArrayMapping('batch', 'qseq', 'nhead', 'head')
  input_sharding[2] = ArrayMapping(*input_sharding[2], 'v')

  # The major dimensions are sharded like the query, the minor like the value.
  output_sharding = (ArrayMapping(*input_sharding[0][:-1], 'v'),)
  if is_fp8:
    # `amax` is a scalar.
    amax = ArrayMapping(f'{BATCHING}{num_args}')
    output_sharding += (amax, amax)
  factor_sizes = {}
  if is_training:
    # Activation sharding.
    if result_types[-1].shape[0] == value_types[0].shape[0]:
      output_sharding += (ArrayMapping('batch', 'nhead', 'qseq'),)
    else:
      factor_sizes['n'] = result_types[-1].shape[0] // value_types[0].shape[0]
      output_sharding += (ArrayMapping(CompoundFactor('batch', 'n'), 'nhead', 'qseq'),)
  return SdyShardingRule(tuple(input_sharding), output_sharding, **factor_sizes)

