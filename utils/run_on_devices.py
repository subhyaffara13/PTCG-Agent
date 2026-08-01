
def run_on_devices(*enabled_devices, skip_reason=None):
  """A decorator for test methods to run the test only on certain devices.

  Args:
    *enabled_devices: Device names that the test should run on.
    skip_reason: Optional custom skip message when test is skipped.
  """
  if skip_reason is None:
    skip_reason = (
      "Skipped unless running on devices with tags: " + ", ".join(enabled_devices)
    )
  return _device_filter(lambda: test_device_matches(enabled_devices), skip_reason)

