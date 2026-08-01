
def _get_params_dict(inputs):
  if isinstance(inputs, (dict, flax.core.FrozenDict)):
    return flax.core.unfreeze(inputs)
  else:
    raise ValueError(
      'Can only traverse a flax Model instance or a nested dict, not '
      f'{type(inputs)}'
    )

