
def _add_guardrails_from_policies_in_metadata(
    key_metadata: Optional[dict],
    team_metadata: Optional[dict],
    data: dict,
    metadata_variable_name: str,
    project_metadata: Optional[dict] = None,
) -> None:
    """
    Helper to resolve guardrails from policies attached to key/team/project metadata.

    This function:
    1. Gets policy names from key, team, and project metadata
    2. Resolves guardrails from those policies (including inheritance)
    3. Adds resolved guardrails to request metadata

    Args:
        key_metadata: The key metadata dictionary to check for policies
        team_metadata: The team metadata dictionary to check for policies
        data: The request data to update
        metadata_variable_name: The name of the metadata field in data
        project_metadata: The project metadata dictionary to check for policies
    """
    from litellm._logging import verbose_proxy_logger
    from litellm.proxy.policy_engine.policy_registry import get_policy_registry
    from litellm.proxy.policy_engine.policy_resolver import PolicyResolver
    from litellm.proxy.utils import _premium_user_check
    from litellm.types.proxy.policy_engine import PolicyMatchContext

    # Collect policy names from key and team metadata
    policy_names: set = set()

    # Add key-level policies first
    if key_metadata and "policies" in key_metadata:
        if (
            isinstance(key_metadata["policies"], list)
            and len(key_metadata["policies"]) > 0
        ):
            _premium_user_check()
            policy_names.update(key_metadata["policies"])

    # Add team-level policies
    if team_metadata and "policies" in team_metadata:
        if (
            isinstance(team_metadata["policies"], list)
            and len(team_metadata["policies"]) > 0
        ):
            _premium_user_check()
            policy_names.update(team_metadata["policies"])

    # Add project-level policies
    if project_metadata and "policies" in project_metadata:
        if (
            isinstance(project_metadata["policies"], list)
            and len(project_metadata["policies"]) > 0
        ):
            _premium_user_check()
            policy_names.update(project_metadata["policies"])

    if not policy_names:
        return

    verbose_proxy_logger.debug(
        f"Policy engine: resolving guardrails from key/team policies: {policy_names}"
    )

    # Check if policy registry is initialized
    registry = get_policy_registry()
    if not registry.is_initialized():
        verbose_proxy_logger.debug(
            "Policy engine not initialized, skipping policy resolution from metadata"
        )
        return

    # Build context for policy resolution (model from request data)
    context = PolicyMatchContext(model=data.get("model"))

    # Get all policies from registry
    all_policies = registry.get_all_policies()

    # Resolve guardrails from the specified policies
    resolved_guardrails: set = set()
    for policy_name in policy_names:
        if registry.has_policy(policy_name):
            resolved_policy = PolicyResolver.resolve_policy_guardrails(
                policy_name=policy_name,
                policies=all_policies,
                context=context,
            )
            resolved_guardrails.update(resolved_policy.guardrails)
            verbose_proxy_logger.debug(
                f"Policy engine: resolved guardrails from policy '{policy_name}': {resolved_policy.guardrails}"
            )
        else:
            verbose_proxy_logger.warning(
                f"Policy engine: policy '{policy_name}' not found in registry"
            )

    if not resolved_guardrails:
        return

    # Add resolved guardrails to request metadata
    if metadata_variable_name not in data:
        data[metadata_variable_name] = {}

    existing_guardrails = data[metadata_variable_name].get("guardrails", [])
    if not isinstance(existing_guardrails, list):
        existing_guardrails = []

    # Combine existing guardrails with policy-resolved guardrails (no duplicates)
    combined = set(existing_guardrails)
    combined.update(resolved_guardrails)
    data[metadata_variable_name]["guardrails"] = list(combined)

    # Store applied policies in metadata for tracking
    if "applied_policies" not in data[metadata_variable_name]:
        data[metadata_variable_name]["applied_policies"] = []
    data[metadata_variable_name]["applied_policies"].extend(list(policy_names))

    verbose_proxy_logger.debug(
        f"Policy engine: added guardrails from key/team policies to request metadata: {list(resolved_guardrails)}"
    )

