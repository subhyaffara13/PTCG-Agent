from typing import Any, Optional

def _guardrail_modification_check(
    request_body: dict, team_object: Optional[LiteLLM_TeamTable]
) -> None:
    """
    Reject user-supplied metadata flags that would modify guardrail behavior
    unless the team has explicit permission. Checked keys include the plural
    ``guardrails`` list plus the per-request toggles that influence whether
    default-on guardrails run (``disable_global_guardrails``,
    ``disable_global_guardrail`` singular, and ``opted_out_global_guardrails``).

    User-supplied values for the bypass toggles are also silently ignored by
    ``_get_admin_metadata`` at read time; this check adds defense in depth by
    failing loudly at the auth layer so operators see an explicit 403 instead
    of a confusing silent-ignore.
    """
    from litellm.proxy.guardrails.guardrail_helpers import can_modify_guardrails

    def _coerce_to_dict(container: Any) -> Optional[dict]:
        """Accept dict or JSON-string (from multipart/form-data or extra_body).

        Without this, an attacker can smuggle guardrail keys past the check by
        sending ``{"metadata": "{\\"disable_global_guardrails\\": true}"}`` —
        ``isinstance(dict)`` on the string returns False, the check returns
        no-modification, and ``add_litellm_data_to_request`` parses the string
        to a dict downstream.
        """
        if isinstance(container, dict):
            return container
        if isinstance(container, str):
            parsed = safe_json_loads(container)
            return parsed if isinstance(parsed, dict) else None
        return None

    def _user_requested_modification(container: Any) -> bool:
        coerced = _coerce_to_dict(container)
        if coerced is None:
            return False
        return any(key in coerced for key in _GUARDRAIL_MODIFICATION_KEYS)

    # Check both metadata keys — callers can populate either depending on the
    # endpoint. Cover the top-level too so root-level injection is rejected.
    modifies = (
        _user_requested_modification(request_body.get("metadata"))
        or _user_requested_modification(request_body.get("litellm_metadata"))
        or _user_requested_modification(request_body)
    )
    if not modifies:
        return

    if not can_modify_guardrails(team_object):
        raise HTTPException(
            status_code=403,
            detail={
                "error": "Your team does not have permission to modify guardrails."
            },
        )

