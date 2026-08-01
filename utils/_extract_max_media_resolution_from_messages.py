
def _extract_max_media_resolution_from_messages(
    messages: List[AllMessageValues],
) -> Optional[str]:
    """
    Extract the highest media resolution (detail) from image content in messages.

    This is used to set the global media_resolution in generation_config for
    Gemini 2.x models which don't support per-part media resolution.

    Args:
        messages: List of messages in OpenAI format

    Returns:
        The highest detail level found ("high", "low", or None)
    """
    max_resolution: Optional[str] = None
    for msg in messages:
        content = msg.get("content")
        if isinstance(content, list):
            for item in content:
                if not isinstance(item, dict):
                    continue
                detail: Optional[str] = None
                if item.get("type") == "image_url":
                    image_url = item.get("image_url")
                    if isinstance(image_url, dict):
                        detail = image_url.get("detail")
                elif item.get("type") == "file":
                    file_obj = item.get("file")
                    if isinstance(file_obj, dict):
                        detail = file_obj.get("detail")
                if detail:
                    max_resolution = _get_highest_media_resolution(
                        max_resolution, detail
                    )
    return max_resolution

