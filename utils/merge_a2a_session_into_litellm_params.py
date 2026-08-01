
def merge_a2a_session_into_litellm_params(
    litellm_params: Dict[str, Any],
    params: Dict[str, Any],
    principal: Optional[str] = None,
) -> Dict[str, Any]:
    merged = dict(litellm_params)
    session_id = get_session_id_from_a2a_params(params)
    if session_id and "session_id" not in merged:
        merged["session_id"] = scope_session_to_principal(session_id, principal)
    return merged

