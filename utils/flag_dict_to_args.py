from typing import Any

def flag_dict_to_args(
    flag_map: dict[str, Any], multi_flags: set[str] | None = None
) -> Iterable[str]:
  """Convert a dict of values into process call parameters.

  This method is used to convert a dictionary into a sequence of parameters
  for a binary that parses arguments using this module.

  Args:
    flag_map: dict, a mapping where the keys are flag names (strings).
        values are treated according to their type:

        * If value is ``None``, then only the name is emitted.
        * If value is ``True``, then only the name is emitted.
        * If value is ``False``, then only the name prepended with 'no' is
          emitted.
        * If value is a string then ``--name=value`` is emitted.
        * If value is a collection, this will emit
          ``--name=value1,value2,value3``, unless the flag name is in
          ``multi_flags``, in which case this will emit
          ``--name=value1 --name=value2 --name=value3``.
        * Everything else is converted to string an passed as such.

    multi_flags: set, names (strings) of flags that should be treated as
        multi-flags.
  Yields:
    sequence of string suitable for a subprocess execution.
  """
  for key, value in flag_map.items():
    if value is None:
      yield '--%s' % key
    elif isinstance(value, bool):
      if value:
        yield '--%s' % key
      else:
        yield '--no%s' % key
    elif isinstance(value, (bytes, str)):
      # We don't want strings to be handled like python collections.
      yield '--%s=%s' % (key, value)  # type: ignore[str-bytes-safe]
    else:
      # Now we attempt to deal with collections.
      try:
        if multi_flags and key in multi_flags:
          for item in value:
            yield '--%s=%s' % (key, str(item))
        else:
          yield '--%s=%s' % (key, ','.join(str(item) for item in value))
      except TypeError:
        # Default case.
        yield '--%s=%s' % (key, value)

