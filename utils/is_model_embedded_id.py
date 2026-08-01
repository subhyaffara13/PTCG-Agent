
def is_model_embedded_id(file_id: str) -> bool:
    """
    Check if a file/batch ID has model routing information embedded.
    """
    return decode_model_from_file_id(file_id) is not None

