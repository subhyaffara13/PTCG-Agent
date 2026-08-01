
def device_under_test() -> str:
  return _TEST_DUT.value or xla_bridge.get_backend().platform

