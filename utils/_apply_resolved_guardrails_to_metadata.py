from typing import Any, Dict, List, Optional

def _apply_resolved_guardrails_to_metadata(
    data: dict,
    metadata_variable_name: str,
    context: "PolicyMatchContext",
    policy_names: Optional[List[str]] = None,
    policies: Optional[Dict[str, Any]] = None,
) -> None:
    """Apply resolved guardrails and pipelines to request metadata."""
    from litellm._logging import verbose_proxy_logger
    from litellm.proxy.policy_engine.policy_resolver import PolicyResolver

    # Resolve guardrails from matching policies
    resolved_guardrails = PolicyResolver.resolve_guardrails_for_context(
        context=context,
        policies=policies,
        policy_names=policy_names,
    )

    verbose_proxy_logger.debug(
        f"Policy engine: resolved guardrails: {resolved_guardrails}"
    )

    # Resolve pipelines from matching policies
    pipelines = PolicyResolver.resolve_pipelines_for_context(
        context=context,
        policies=policies,
        policy_names=policy_names,
    )

    # Add resolved guardrails to request metadata
    if metadata_variable_name not in data:
        data[metadata_variable_name] = {}

    # Track pipeline-managed guardrails to exclude from independent execution
    pipeline_managed_guardrails: set = set()
    if pipelines:
        pipeline_managed_guardrails = PolicyResolver.get_pipeline_managed_guardrails(
            pipelines
        )
        data[metadata_variable_name]["_guardrail_pipelines"] = pipelines
        data[metadata_variable_name][
            "_pipeline_managed_guardrails"
        ] = pipeline_managed_guardrails
        verbose_proxy_logger.debug(
            f"Policy engine: resolved {len(pipelines)} pipeline(s), "
            f"managed guardrails: {pipeline_managed_guardrails}"
        )

    if not resolved_guardrails and not pipelines:
        return

    existing_guardrails = data[metadata_variable_name].get("guardrails", [])
    if not isinstance(existing_guardrails, list):
        existing_guardrails = []

    # Combine existing guardrails with policy-resolved guardrails (no duplicates)
    # Exclude pipeline-managed guardrails from the flat list
    combined = set(existing_guardrails)
    combined.update(resolved_guardrails)
    combined -= pipeline_managed_guardrails
    data[metadata_variable_name]["guardrails"] = list(combined)

    verbose_proxy_logger.debug(
        f"Policy engine: added guardrails to request metadata: {list(combined)}"
    )

