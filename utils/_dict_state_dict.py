
def _dict_state_dict(xs: dict[str, Any]) -> dict[str, Any]:
  str_keys = {str(k) for k in xs.keys()}
  if len(str_keys) != len(xs):
    raise ValueError(
      'Dict keys do not have a unique string representation: '
      f'{str_keys} vs given: {xs}'
    )
  return {str(key): to_state_dict(value) for key, value in xs.items()}

