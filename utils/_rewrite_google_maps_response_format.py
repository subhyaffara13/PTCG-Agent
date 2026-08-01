
def _rewrite_google_maps_response_format(data: RequestBody) -> None:
    generation_config = cast(Optional[GenerationConfig], data.get("generationConfig"))
    if (
        isinstance(generation_config, dict)
        and _has_google_maps_tool(data.get("tools"))
        and generation_config.get("response_mime_type") == "application/json"
    ):
        _rewrite_mime_type_to_response_format(generation_config)

