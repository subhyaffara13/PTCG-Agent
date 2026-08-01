
def _is_multimodal_element(element: str) -> bool:
    """Check if a single string element is multimodal."""
    if element.startswith("data:") and ";base64," in element:
        return True
    if _is_file_reference(element):
        return True
    if _is_gcs_url(element):
        return True
    return False

