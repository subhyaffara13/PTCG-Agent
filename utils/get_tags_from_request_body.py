from typing import Any, List

def get_tags_from_request_body(request_body: dict) -> List[str]:
    """
    Extract tags from request body metadata.

    Args:
        request_body: The request body dictionary

    Returns:
        List of tag names (strings), empty list if no valid tags found
    """
    metadata_variable_name = get_metadata_variable_name_from_kwargs(request_body)
    metadata = request_body.get(metadata_variable_name)
    # metadata can arrive as a JSON string from multipart/form-data or extra_body;
    # coerce defensively so .get() below never raises AttributeError.
    if isinstance(metadata, str):
        from litellm.litellm_core_utils.safe_json_loads import safe_json_loads

        parsed = safe_json_loads(metadata)
        metadata = parsed if isinstance(parsed, dict) else {}
    elif not isinstance(metadata, dict):
        metadata = {}
    tags_in_metadata: Any = metadata.get("tags", [])
    tags_in_request_body: Any = request_body.get("tags", [])
    combined_tags: List[str] = []

    ######################################
    # Only combine tags if they are lists
    ######################################
    if isinstance(tags_in_metadata, list):
        combined_tags.extend(tags_in_metadata)
    if isinstance(tags_in_request_body, list):
        combined_tags.extend(tags_in_request_body)
    ######################################
    return [tag for tag in combined_tags if isinstance(tag, str)]

