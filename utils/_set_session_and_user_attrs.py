
def _set_session_and_user_attrs(
    span: "Span", kwargs: dict, standard_logging_payload
) -> None:
    """Emit `SESSION_ID` / `USER_ID` / team metadata when source data exists.

    `SESSION_ID` is emitted only when an explicit end-user identifier exists
    (`metadata.user_api_key_end_user_id`). We deliberately do NOT fall back
    to `trace_id`, because that would create a distinct "session" for every
    single request and distort Arize's Session-grouping analytics. The
    `trace_id` is still emitted under its own `litellm.trace_id` key so
    spans remain filterable by trace.

    USER_ID is *only* emitted when no upstream path (model_params.user or
    optional_params.user) has already set it, to avoid overwriting an
    existing value with a possibly-different one from API-key metadata.
    """
    if not isinstance(standard_logging_payload, dict):
        return
    metadata = standard_logging_payload.get("metadata") or {}
    if not isinstance(metadata, dict):
        return

    session_id = metadata.get("user_api_key_end_user_id")
    if session_id:
        safe_set_attribute(span, SpanAttributes.SESSION_ID, str(session_id))

    trace_id = standard_logging_payload.get("trace_id")
    if trace_id:
        safe_set_attribute(span, "litellm.trace_id", str(trace_id))

    optional_params = kwargs.get("optional_params") or {}
    model_params = standard_logging_payload.get("model_parameters") or {}
    has_user_already = bool(
        (isinstance(optional_params, dict) and optional_params.get("user"))
        or (isinstance(model_params, dict) and model_params.get("user"))
    )
    if not has_user_already:
        user_id = metadata.get("user_api_key_user_id")
        if user_id:
            safe_set_attribute(span, SpanAttributes.USER_ID, str(user_id))

    team_id = metadata.get("user_api_key_team_id")
    if team_id:
        safe_set_attribute(span, "litellm.team_id", str(team_id))
    team_alias = metadata.get("user_api_key_team_alias")
    if team_alias:
        safe_set_attribute(span, "litellm.team_alias", str(team_alias))
    key_alias = metadata.get("user_api_key_alias")
    if key_alias:
        safe_set_attribute(span, "litellm.key_alias", str(key_alias))

