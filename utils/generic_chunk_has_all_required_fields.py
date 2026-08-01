
def generic_chunk_has_all_required_fields(chunk: dict) -> bool:
    """
    Checks if the provided chunk dictionary contains all required fields for GenericStreamingChunk.

    :param chunk: The dictionary to check.
    :return: True if all required fields are present, False otherwise.
    """
    return all(key in _GCHUNK_FIELDS for key in chunk)

