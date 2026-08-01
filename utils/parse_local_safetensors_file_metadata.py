
def parse_local_safetensors_file_metadata(path: str | Path) -> SafetensorsFileMetadata:
    """
    Parse metadata from a local safetensors file.

    For more details regarding the safetensors format, check out https://huggingface.co/docs/safetensors/index#format.

    Args:
        path (`str` or `Path`):
            Path to the safetensors file.

    Returns:
        [`SafetensorsFileMetadata`]: information related to the safetensors file.

    Raises:
        [`SafetensorsParsingError`]:
            If the safetensors file header couldn't be parsed correctly.
        `FileNotFoundError`:
            If the file does not exist.

    Example:
        ```py
        >>> metadata = parse_local_safetensors_file_metadata("path/to/model.safetensors")
        >>> metadata
        SafetensorsFileMetadata(
            metadata={'format': 'pt'},
            tensors={'layer.weight': TensorInfo(dtype='F32', shape=[512, 512], ...}, ...}
        )
        >>> metadata.parameter_count
        {'F32': 262144}
        ```
    """
    path = Path(path)
    filename = path.name
    context_msg = f"path '{path}'"

    with open(path, "rb") as f:
        # 1. Read first 8 bytes and parse/validate metadata size using shared helper
        size_bytes = f.read(8)
        metadata_size = _get_safetensors_metadata_size(size_bytes, filename, context_msg)

        # 2. Read metadata bytes
        metadata_as_bytes = f.read(metadata_size)
        if len(metadata_as_bytes) < metadata_size:
            raise SafetensorsParsingError(
                f"Failed to parse safetensors header for '{filename}' ({context_msg}): file is truncated. Expected "
                f"{metadata_size} bytes of metadata but got {len(metadata_as_bytes)}."
            )

    # 3. Parse using shared helper
    return _parse_safetensors_header(metadata_as_bytes, filename, context_msg)

