
def _pool() -> descriptor_pool.DescriptorPool:
  """Returns a descriptor pool with all registered protos."""
  return symbol_database.Default().pool

