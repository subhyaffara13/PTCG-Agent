
def _replace_file_id_in_response(response, original_file_id: str):
    """
    Replace the provider file ID in the response with the original managed file ID.

    This ensures that when a user sends a managed file ID, they get back the same
    managed file ID in the response, not the decoded provider file ID.

    Args:
        response: The response object from the provider
        original_file_id: The original managed file ID to restore

    Returns:
        Modified response with original file ID
    """
    if response is None:
        return response

    # Handle different response types
    if isinstance(response, dict):
        # For dict responses (e.g., VectorStoreFileDeleteResponse)
        if "id" in response:
            response["id"] = original_file_id
        if "file_id" in response:
            response["file_id"] = original_file_id
    elif hasattr(response, "id"):
        # For object responses (e.g., VectorStoreFileObject)
        response.id = original_file_id
    elif hasattr(response, "file_id"):
        response.file_id = original_file_id

    return response

