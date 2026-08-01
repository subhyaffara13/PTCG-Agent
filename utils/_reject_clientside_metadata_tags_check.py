
def _reject_clientside_metadata_tags_check(
    general_settings: dict, request_body: dict, route: str
) -> None:
    if not general_settings.get("reject_clientside_metadata_tags", False):
        return

    if (
        RouteChecks.is_llm_api_route(route=route)
        and "metadata" in request_body
        and isinstance(request_body["metadata"], dict)
        and "tags" in request_body["metadata"]
    ):
        raise ProxyException(
            message=f"Client-side 'metadata.tags' not allowed in request. 'reject_clientside_metadata_tags'={general_settings['reject_clientside_metadata_tags']}. Tags can only be set via API key metadata.",
            type=ProxyErrorTypes.bad_request_error,
            param="metadata.tags",
            code=status.HTTP_400_BAD_REQUEST,
        )

