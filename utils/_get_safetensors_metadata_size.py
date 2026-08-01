
def _get_safetensors_metadata_size(size_bytes: bytes, filename: str, context_msg: str) -> int:
    """
    Parse and validate safetensors metadata size from the first 8 bytes.

    This is a shared helper function used by both remote and local safetensors parsing.

    Args:
        size_bytes: First 8 bytes of the safetensors file.
        filename: Filename for error messages.
        context_msg: Additional context for error messages.

    Returns:
        The metadata size as an integer.

    Raises:
        SafetensorsParsingError: If size_bytes is too short or metadata size exceeds limit.
    """
    if len(size_bytes) < 8:
        raise SafetensorsParsingError(
            f"Failed to parse safetensors header for '{filename}' ({context_msg}): file is too small to be a valid "
            "safetensors file."
        )

    metadata_size = struct.unpack("<Q", size_bytes[:8])[0]
    if metadata_size > constants.SAFETENSORS_MAX_HEADER_LENGTH:
        raise SafetensorsParsingError(
            f"Failed to parse safetensors header for '{filename}' ({context_msg}): safetensors header is too big. "
            f"Maximum supported size is {constants.SAFETENSORS_MAX_HEADER_LENGTH} bytes (got {metadata_size})."
        )

    return metadata_size

