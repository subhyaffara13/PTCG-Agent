from typing import Any

def restore_flag_values(
    saved_flag_values: Mapping[str, dict[str, Any]],
    flag_values: flags.FlagValues = FLAGS,
) -> None:
  """Restores flag values based on the dictionary of flag values.

  Args:
    saved_flag_values: {'flag_name': value_dict, ...}
    flag_values: FlagValues, the FlagValues instance from which the flag will be
      restored. This should almost never need to be overridden.
  """
  new_flag_names = list(flag_values)
  for name in new_flag_names:
    saved = saved_flag_values.get(name)
    if saved is None:
      # If __dict__ was not saved delete "new" flag.
      delattr(flag_values, name)
    else:
      if flag_values[name].value != saved['_value']:
        flag_values[name].value = saved['_value']  # Ensure C++ value is set.
      flag_values[name].__dict__ = saved

