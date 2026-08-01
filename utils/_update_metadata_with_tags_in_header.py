
def _update_metadata_with_tags_in_header(request: Request, metadata: dict) -> dict:
    """
    If tags are in the request headers, add them to the metadata

    Used for google and vertex JS SDKs, and Azure passthrough
    Checks both 'tags' and 'x-litellm-tags' headers
    """
    tags_to_add = []

    # Check for 'tags' header first
    _tags = request.headers.get("tags")
    if _tags:
        tags_to_add.extend([tag.strip() for tag in _tags.split(",")])

    _tags = request.headers.get("x-litellm-tags")
    if _tags:
        tags_to_add.extend([tag.strip() for tag in _tags.split(",")])

    # Only add tags key if there are tags to add
    if tags_to_add:
        if "tags" not in metadata:
            metadata["tags"] = []
        metadata["tags"].extend(tags_to_add)

    return metadata

