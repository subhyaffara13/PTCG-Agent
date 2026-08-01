
def get_sparse_core_info() -> tpu_info.SparseCoreInfo:
  """Returns the SparseCore information for the current device.

  Raises:
    RuntimeError: If the current TPU does not have SparseCores.
  """
  sc_info = tpu_info.get_tpu_info().sparse_core
  if sc_info is None:
    raise RuntimeError("The current TPU does not have SparseCores")
  return sc_info

