
def metadata_store(
    *,
    enable_write: bool,
    blocking_write: bool = False,
) -> MetadataStore:
  """Returns `MetadataStore` instance based on `enable_write` value.

  Write operations are thread safe: within a process multiple threads write
  without corrupting data.

  NOTE: Write operations are not guaranteed to be safe across processes. But it
  should be okay as writes are expected to be called from just one jax process.

  Read operations are inherently thread safe and *process safe* too.

  NOTE: `MetadataStore` instance created with `enable_write=True`
  and `blocking_write=False` must be closed with `.close()` to release thread
  resources. Prefer to reuse an instance created for this scenario.

  Args:
    enable_write: if True then write operations are allowed, otherwise write
      operations are **no op**. Read operations are always allowed.
    blocking_write: if True then write operations are blocking, otherwise non
      blocking. Read responses don't reflect in progress writes.
  """
  if not blocking_write:
    if enable_write:
      return _NonBlockingMetadataStore(enable_write=True)
    return _METADATA_STORE_NON_BLOCKING_FOR_READS

  if enable_write:
    return _METADATA_STORE_FOR_WRITES
  return _METADATA_STORE_FOR_READS

