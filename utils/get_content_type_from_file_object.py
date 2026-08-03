from typing import Optional

def get_content_type_from_file_object(file_object: Optional[dict]) -> str:
    """
    Determine content type from file object (from database or API response).

    Extracts filename from file object and uses detect_content_type_from_filename.
    Falls back to default if file object is invalid or filename not found.

    Args:
        file_object: File object dictionary (can be None)

    Returns:
        str: MIME type (defaults to "application/octet-stream" if cannot be determined)
    """
    if not file_object:
        return "application/octet-stream"

    # Handle JSON string
    if isinstance(file_object, str):
        import json

        try:
            file_object = json.loads(file_object)
        except json.JSONDecodeError:
            return "application/octet-stream"

    if not isinstance(file_object, dict):
        return "application/octet-stream"

    # Try to get filename
    filename = file_object.get("filename", "")
    if filename:
        return detect_content_type_from_filename(filename)

    return "application/octet-stream"

