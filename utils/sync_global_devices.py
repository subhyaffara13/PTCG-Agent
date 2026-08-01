
def sync_global_devices(name: str):
  """Creates a barrier across all hosts/devices."""
  h = np.uint32(zlib.crc32(name.encode()))
  assert_equal(h, f"sync_global_devices name mismatch ('{name}')")

