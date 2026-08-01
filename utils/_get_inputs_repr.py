
def _get_inputs_repr(args, kwargs):
  input_args, input_kwargs = jax.tree.map(
    _to_dummy_array, (args, kwargs)
  )
  inputs_repr = ''
  if input_args:
    if len(input_args) == 1 and not input_kwargs:
      inputs_repr += _as_yaml_str(input_args[0])
    else:
      inputs_repr += _as_yaml_str(input_args)
    if input_kwargs:
      inputs_repr += '\n'
  if input_kwargs:
    inputs_repr += _as_yaml_str(input_kwargs)
  return inputs_repr

