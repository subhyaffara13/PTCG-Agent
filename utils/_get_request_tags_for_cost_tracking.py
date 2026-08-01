
def _get_request_tags_for_cost_tracking(
    sl_object: Optional[StandardLoggingPayload],
    metadata: dict,
) -> Optional[List[str]]:
    if sl_object is not None:
        request_tags = sl_object.get("request_tags", None)
        if isinstance(request_tags, list):
            return request_tags

    metadata_tags = metadata.get("tags", None)
    if isinstance(metadata_tags, list):
        return metadata_tags

    return None

