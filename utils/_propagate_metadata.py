from typing import Any, Dict, Optional

def _propagate_metadata(
    parent_litellm_metadata: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Extract the parent request's auth/spend-attribution fields for the summary subcall.

    The proxy attaches ``user_api_key``, ``user_api_key_team_id`` etc. to
    ``data["litellm_metadata"]`` (see
    ``LiteLLMProxyRequestSetup.add_user_api_key_auth_to_request_metadata``).
    Without these on the summary subrequest, the router's post-call hooks
    cannot attribute summary tokens to the caller's key/team budget.
    """
    if not parent_litellm_metadata:
        return {}
    propagated: Dict[str, Any] = {}
    for key in _PROPAGATED_METADATA_KEYS:
        if key in parent_litellm_metadata:
            propagated[key] = parent_litellm_metadata[key]
    return propagated

