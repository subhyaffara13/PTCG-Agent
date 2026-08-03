from typing import Any, Dict, Optional

def _match_and_track_policies(
    data: dict,
    context: "PolicyMatchContext",
    request_body_policies: Any,
    policies_override: Optional[Dict[str, Any]] = None,
) -> tuple[list[str], dict[str, str]]:
    """
    Match policies via attachments and request body, track them in metadata.

    Returns:
        Tuple of (applied_policy_names, policy_reasons)
    """
    from litellm._logging import verbose_proxy_logger
    from litellm.proxy.common_utils.callback_utils import (
        add_policy_sources_to_metadata,
        add_policy_to_applied_policies_header,
    )
    from litellm.proxy.policy_engine.attachment_registry import get_attachment_registry
    from litellm.proxy.policy_engine.policy_matcher import PolicyMatcher

    # Get matching policies via attachments (with match reasons for attribution)
    attachment_registry = get_attachment_registry()
    matches_with_reasons = attachment_registry.get_attached_policies_with_reasons(
        context
    )
    matching_policy_names = [m["policy_name"] for m in matches_with_reasons]
    policy_reasons = {m["policy_name"]: m["matched_via"] for m in matches_with_reasons}

    verbose_proxy_logger.debug(
        f"Policy engine: matched policies via attachments: {matching_policy_names}"
    )

    # Combine attachment-based policies with dynamic request body policies
    all_policy_names = set(matching_policy_names)
    if request_body_policies and isinstance(request_body_policies, list):
        all_policy_names.update(request_body_policies)
        verbose_proxy_logger.debug(
            f"Policy engine: added dynamic policies from request body: {request_body_policies}"
        )

    if not all_policy_names:
        return [], {}

    # Filter to only policies whose conditions match the context
    applied_policy_names = PolicyMatcher.get_policies_with_matching_conditions(
        policy_names=list(all_policy_names),
        context=context,
        policies=policies_override,
    )

    verbose_proxy_logger.debug(
        f"Policy engine: applied policies (conditions matched): {applied_policy_names}"
    )

    # Track applied policies in metadata for response headers
    for policy_name in applied_policy_names:
        add_policy_to_applied_policies_header(
            request_data=data, policy_name=policy_name
        )

    # Track policy attribution sources for x-litellm-policy-sources header
    applied_reasons = {
        name: policy_reasons[name]
        for name in applied_policy_names
        if name in policy_reasons
    }
    add_policy_sources_to_metadata(request_data=data, policy_sources=applied_reasons)

    return applied_policy_names, policy_reasons

