
def _MakeDefaultOrNone(kls, config, allow_none=True, field_path=''):
  if config in ['build', True]:
    try:
      return kls()
    except Exception as e:
      raise ValueError(
          f'Unable to create default instance for "{field_path}" '
          f'of type "{kls}": {e}') from e

  elif (config in ['0', 0, False] or config.lower() == 'none'):
    if not allow_none:
      raise ValueError(f'None is not allowed as value for "{field_path}", '
                       'as the dataclass field is not marked as optional.')
    return None
  raise ValueError(f'Unable to parse value "{config}" as instance of {kls}'
                   f'for {field_path} values allowed are [0/none, or 1]')

