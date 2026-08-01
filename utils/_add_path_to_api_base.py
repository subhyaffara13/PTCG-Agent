
def _add_path_to_api_base(api_base: str, ending_path: str) -> str:
    """
    Adds an ending path to an API base URL while preventing duplicate path segments.

    Args:
        api_base: Base URL string
        ending_path: Path to append to the base URL

    Returns:
        Modified URL string with proper path handling
    """
    original_url = httpx.URL(api_base)
    base_url = original_url.copy_with(params={})  # Removes query params
    base_path = original_url.path.rstrip("/")
    end_path = ending_path.lstrip("/")

    # Split paths into segments
    base_segments = [s for s in base_path.split("/") if s]
    end_segments = [s for s in end_path.split("/") if s]

    # Find overlapping segments from the end of base_path and start of ending_path
    final_segments = []
    for i in range(len(base_segments)):
        if base_segments[i:] == end_segments[: len(base_segments) - i]:
            final_segments = base_segments[:i] + end_segments
            break
    else:
        # No overlap found, just combine all segments
        final_segments = base_segments + end_segments

    # Construct the new path
    modified_path = "/" + "/".join(final_segments)
    modified_url = base_url.copy_with(path=modified_path)

    # Re-add the original query parameters
    return str(modified_url.copy_with(params=original_url.params))

