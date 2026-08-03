from typing import Dict

def _convert_image_to_gemini_format(image_file) -> Dict[str, str]:
    """
    Convert image file to Gemini format with base64 encoding and MIME type.

    Args:
        image_file: File-like object opened in binary mode (e.g., open("path", "rb"))

    Returns:
        Dict with bytesBase64Encoded and mimeType
    """
    mime_type = ImageEditRequestUtils.get_image_content_type(image_file)

    if hasattr(image_file, "seek"):
        image_file.seek(0)
    image_bytes = image_file.read()
    base64_encoded = base64.b64encode(image_bytes).decode("utf-8")

    return {"bytesBase64Encoded": base64_encoded, "mimeType": mime_type}

