
def _read_tensor_data(
    f,
    start_offset: int,
    end_offset: int,
    metadata_size: int,
) -> bytes:
    """
    Read a specific byte range of tensor data from an open safetensors file.

    Args:
        f: An open file object (handle) for the safetensors file
        start_offset: Start offset of tensor data within the data section
        end_offset: End offset of tensor data within the data section
        metadata_size: Size of the metadata header

    Returns:
        Raw tensor data as bytes
    """
    absolute_start = metadata_size + start_offset
    length = end_offset - start_offset

    f.seek(absolute_start)
    return f.read(length)

