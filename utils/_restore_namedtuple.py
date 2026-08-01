
def _restore_namedtuple(xs, state_dict: dict[str, Any]):
  """Rebuild namedtuple from serialized dict."""
  if set(state_dict.keys()) == {'name', 'fields', 'values'}:
    # TODO(jheek): remove backward compatible named tuple restoration early 2022
    state_dict = {
      state_dict['fields'][str(i)]: state_dict['values'][str(i)]
      for i in range(len(state_dict['fields']))
    }

  sd_keys = set(state_dict.keys())
  nt_keys = set(xs._fields)

  if sd_keys != nt_keys:
    raise ValueError(
      'The field names of the state dict and the named tuple do not match,'
      f' got {sd_keys} and {nt_keys} at path {current_path()}'
    )
  fields = {
    k: from_state_dict(getattr(xs, k), v, name=k) for k, v in state_dict.items()
  }
  return type(xs)(**fields)

