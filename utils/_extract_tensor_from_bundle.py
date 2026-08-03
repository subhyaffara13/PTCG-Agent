from typing import Any

def _extract_tensor_from_bundle(
    info: dict[str, Any],
    bundle_bytes: bytes,
    bundle_start_offset: int,
    shape: tuple[int, ...],
    dtype: np.dtype,
) -> np.ndarray:
  """Extracts tensor data from the read buffer."""
  start_offset, end_offset = info["data_offsets"]
  rel_start = start_offset - bundle_start_offset
  rel_end = end_offset - bundle_start_offset
  tensor_mv = memoryview(bundle_bytes)[rel_start:rel_end]
  return np.frombuffer(tensor_mv, dtype=dtype).reshape(shape)

