
def skip_on_devices(*disabled_devices, skip_reason=None):
  """A decorator for test methods to skip the test on certain devices.

  Args:
    *disabled_devices: Device names that the test should skip on.
    skip_reason: Optional custom skip message when test is skipped.
  """
  if skip_reason is None:
    skip_reason = "Skipped on devices with tags: " + ", ".join(disabled_devices)
  return _device_filter(lambda: not test_device_matches(disabled_devices), skip_reason)

