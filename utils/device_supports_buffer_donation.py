
def device_supports_buffer_donation():
  """A decorator for test methods to run the test only on devices that support
  buffer donation."""
  return _device_filter(
      lambda: test_device_matches(mlir._platforms_with_donation)
  )

