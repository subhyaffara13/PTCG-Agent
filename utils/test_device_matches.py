
def test_device_matches(device_types: Iterable[str]) -> bool:
  assert not isinstance(
      device_types, str
  ), 'device_types should be a list of strings'
  tags = _get_device_tags()
  for device_type in device_types:
    assert isinstance(device_type, str), device_type
    if device_type in tags:
      return True
  return False

