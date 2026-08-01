
def single_host_load_and_broadcast_name_format(
    name_format: NameFormat[Metadata],
) -> NameFormat[Metadata]:
  """Returns a name format with single_host_load_and_broadcast enabled."""
  if is_standard_name_format(name_format):
    return dataclasses.replace(name_format, single_host_load_and_broadcast=True)  # pytype: disable=wrong-arg-types
  else:
    raise ValueError(
        'single_host_load_and_broadcast is only supported for standard name'
        f' formats. Got {name_format}.'
    )

