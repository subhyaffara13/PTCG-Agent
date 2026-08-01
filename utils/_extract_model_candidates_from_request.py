
def _extract_model_candidates_from_request(
    request_data: dict,
    route: str,
    request_headers: Optional[Mapping[str, Any]] = None,
    request_query_params: Optional[Mapping[str, Any]] = None,
    llm_router: Optional[Router] = None,
) -> List[str]:
    candidates: List[str] = []
    uses_model_routing_sources = _route_uses_model_routing_sources(route=route)
    uses_header_or_query_model_sources = _route_matches_any_marker(
        route=route, markers=_MODEL_ROUTING_HEADER_OR_QUERY_ROUTE_MARKERS
    )
    uses_query_target_model_sources = _route_matches_any_marker(
        route=route, markers=_MODEL_ROUTING_QUERY_TARGET_MODEL_ROUTE_MARKERS
    )
    uses_body_target_model_sources = _route_matches_any_marker(
        route=route, markers=_MODEL_ROUTING_BODY_TARGET_MODEL_ROUTE_MARKERS
    )
    uses_completion_model_sources = _route_matches_any_marker(
        route=route, markers=_MODEL_ROUTING_COMPLETION_MODEL_ROUTE_MARKERS
    )

    body_model = request_data.get("model")
    _append_model_candidates(candidates, body_model)
    if uses_body_target_model_sources or not body_model:
        _append_model_candidates(candidates, request_data.get("target_model_names"))
    if _route_matches_any_marker(
        route=route, markers=_MODEL_ROUTING_SESSION_MODEL_ROUTE_MARKERS
    ):
        session = request_data.get("session")
        if isinstance(session, dict):
            _append_model_candidates(candidates, session.get("model"))
    if uses_completion_model_sources and isinstance(
        request_data.get("completion"), dict
    ):
        _append_model_candidates(candidates, request_data["completion"].get("model"))

    if uses_model_routing_sources:
        if uses_header_or_query_model_sources:
            _append_model_candidates(
                candidates,
                _get_case_insensitive_mapping_value(request_query_params, "model"),
            )
            _append_model_candidates(
                candidates,
                _get_case_insensitive_mapping_value(
                    request_headers, MODEL_ROUTING_HEADER_NAME
                ),
            )
        if uses_query_target_model_sources:
            _append_model_candidates(
                candidates,
                _get_case_insensitive_mapping_value(
                    request_query_params, "target_model_names"
                ),
            )

        for field in _MODEL_ROUTING_ID_FIELDS:
            _append_model_candidates(
                candidates,
                _extract_models_from_managed_resource_id(
                    request_data.get(field),
                    resource_id_field=field,
                    llm_router=llm_router,
                ),
            )

    return _dedupe_model_candidates(candidates)

