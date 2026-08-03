from typing import Any

def _enforce_inbound_trace_id(agent: Any, request: Request) -> None:
    """Raise 400 if agent requires x-litellm-trace-id on inbound calls and it is missing."""
    agent_litellm_params = agent.litellm_params or {}
    if not agent_litellm_params.get("require_trace_id_on_calls_to_agent"):
        return

    from litellm.proxy.litellm_pre_call_utils import get_chain_id_from_headers

    headers_dict = dict(request.headers)
    trace_id = get_chain_id_from_headers(headers_dict)
    if not trace_id:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Agent '{agent.agent_id}' requires x-litellm-trace-id header "
                "on all inbound requests."
            ),
        )

