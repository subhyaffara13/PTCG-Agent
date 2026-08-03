import os

def _gs_uri_requires_content_type_metadata(url: str) -> bool:
    """
    True when _process_gemini_media would call _get_gcs_object_content_type
    (extension-less gs:// and no explicit format passed into that helper).
    """
    if "gs://" not in url:
        return False
    extension_with_dot = os.path.splitext(url)[-1]
    extension = extension_with_dot[1:] if extension_with_dot else ""
    return len(extension) == 0

