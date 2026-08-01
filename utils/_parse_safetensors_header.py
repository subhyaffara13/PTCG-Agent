
def _parse_safetensors_header(metadata_as_bytes: bytes, filename: str, context_msg: str) -> SafetensorsFileMetadata:
    """
    Parse safetensors metadata from raw header bytes.

    This is a shared helper function used by both remote and local safetensors parsing.

    Args:
        metadata_as_bytes: Raw bytes of the JSON metadata header (without the 8-byte size prefix).
        filename: Filename for error messages.
        context_msg: Additional context for error messages (e.g., repo info or local path).

    Returns:
        SafetensorsFileMetadata object.

    Raises:
        SafetensorsParsingError: If the header cannot be parsed.
    """
    # Parse json header
    try:
        metadata_as_dict = json.loads(metadata_as_bytes.decode(errors="ignore"))
    except json.JSONDecodeError as e:
        raise SafetensorsParsingError(
            f"Failed to parse safetensors header for '{filename}' ({context_msg}): header is not json-encoded string. "
            "Please make sure this is a correctly formatted safetensors file."
        ) from e

    try:
        return SafetensorsFileMetadata(
            metadata=metadata_as_dict.get("__metadata__", {}),
            tensors={
                key: TensorInfo(
                    dtype=tensor["dtype"],
                    shape=tensor["shape"],
                    data_offsets=tuple(tensor["data_offsets"]),  # type: ignore
                )
                for key, tensor in metadata_as_dict.items()
                if key != "__metadata__"
            },
        )
    except (KeyError, IndexError) as e:
        raise SafetensorsParsingError(
            f"Failed to parse safetensors header for '{filename}' ({context_msg}): header format not recognized. "
            "Please make sure this is a correctly formatted safetensors file."
        ) from e

