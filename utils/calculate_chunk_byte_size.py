import math


def calculate_chunk_byte_size(
    write_shape: Shape,
    dtype: DType,
    *,
    chunk_byte_size: int | None,
    ocdbt_target_data_file_size: int | None = None,
    kvstore_spec: JsonSpec | None = None,
) -> int | None:
  """Selects chunk byte size to fit both target data file and chunk sizes."""
  # Check if the chunk size would exceed ocdbt target file size.
  if ocdbt_target_data_file_size is None:
    ocdbt_target_data_file_size = _get_backend_ocdbt_target_data_file_size(
        kvstore_spec
    )

  if ocdbt_target_data_file_size == 0:
    # No limit.
    return chunk_byte_size

  if chunk_byte_size is None:
    write_nbytes = math.prod(write_shape) * dtype.itemsize
    if write_nbytes > ocdbt_target_data_file_size:
      chunk_byte_size = ocdbt_target_data_file_size
    else:
      # Let chunk_byte_size stay None.
      chunk_byte_size = None
  else:
    chunk_byte_size = min(chunk_byte_size, ocdbt_target_data_file_size)
  return chunk_byte_size

